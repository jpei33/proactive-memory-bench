"""Chunker D: LLM topic segmentation per channel.

    python -m memory.segment --ws ando | --all     # writes data/cache/segments_<ws>.json

Per channel, every 20 new messages: send the last 40 (numbered) and keep the boundaries that fall
inside the newest 20. So a boundary can be placed using up to 19 messages that come after it
(limitation: D sees a little of the future when cutting topics; contents are still cut by visible()).
Segments longer than 12 messages are split; each later piece repeats the segment's first message
at the top, marked "[topic start]".
"""
from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from memory.base import Chunk, line, load_msgs, make_chunk

SEGMENT = """Chat messages from one channel, numbered, oldest first:
{NUMBERED}
A new topic starts when people move to a different task, decision or question.
Return JSON only: {"starts": [numbers of messages that begin a new topic]}"""

STEP, CTX, MAX_SEG = 20, 40, 12
CACHE = Path("data/cache")


def _by_channel(msgs):
    by_ch = defaultdict(list)
    for m in msgs:
        by_ch[m["channel"]].append(m)
    return by_ch


def boundaries(msgs: list[dict], workers: int = 8) -> dict:
    """channel -> sorted list of msg_ids that start a topic. Uses the cheap model, disk-cached."""
    from sim.llm import complete, parse_json
    model = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")
    jobs = []
    for ch, ms in _by_channel(msgs).items():
        for end in range(STEP, len(ms) + STEP, STEP):
            end = min(end, len(ms))
            lo = max(0, end - CTX)
            new_from = max(0, end - STEP) - lo        # index (in the numbered list) of the newest block
            jobs.append((ch, ms[lo:end], new_from))
            if end == len(ms):
                break

    def ask(job):
        ch, ctx, new_from = job
        numbered = "\n".join(f"[{i}] {m['speaker']}: {m['text']}" for i, m in enumerate(ctx))
        r = complete(None, SEGMENT.replace("{NUMBERED}", numbered), model=model, max_tokens=200)
        try:
            starts = [int(s) for s in parse_json(r.text).get("starts", [])]
        except (ValueError, AttributeError, TypeError):
            starts = []
        return ch, [ctx[i]["msg_id"] for i in starts if new_from <= i < len(ctx)]

    out = defaultdict(set)
    with ThreadPoolExecutor(workers) as ex:
        for ch, ids in ex.map(ask, jobs):
            out[ch].update(ids)
    for ch, ms in _by_channel(msgs).items():
        out[ch].add(ms[0]["msg_id"])                  # every channel starts a topic
    seq = {m["msg_id"]: m["seq"] for m in msgs}
    return {ch: sorted(ids, key=seq.get) for ch, ids in out.items()}, len(jobs)


def chunk_D(msgs: list[dict], starts: dict) -> list[Chunk]:
    out = []
    for ch, ms in _by_channel(msgs).items():
        bset = set(starts.get(ch, [])) | {ms[0]["msg_id"]}
        segs, cur = [], []
        for m in ms:
            if m["msg_id"] in bset and cur:
                segs.append(cur)
                cur = []
            cur.append(m)
        segs.append(cur)
        for si, seg in enumerate(segs):
            for pi in range(0, len(seg), MAX_SEG):
                piece = seg[pi:pi + MAX_SEG]
                cid = f"D:{ch}:{si}:{pi // MAX_SEG}"
                if pi == 0:
                    out.append(make_chunk(cid, piece))
                else:                                  # repeat the topic's first message on top
                    head = seg[0]
                    out.append(Chunk(cid, (head["msg_id"],) + tuple(m["msg_id"] for m in piece),
                                     head["seq"], piece[-1]["seq"],
                                     "[topic start] " + line(head) + "\n" + "\n".join(line(m) for m in piece)))
    return out


def seg_path(ws):
    return CACHE / f"segments_{ws}.json"


def load_segments(ws):
    p = seg_path(ws)
    return json.loads(p.read_text()) if p.exists() else None


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    for ws in (["ando", "anthropic", "openai", "xai"] if a.all else [a.ws]):
        msgs = load_msgs(ws)
        starts, calls = boundaries(msgs)
        CACHE.mkdir(parents=True, exist_ok=True)
        seg_path(ws).write_text(json.dumps(starts, indent=1))
        D = chunk_D(msgs, starts)
        sizes = [len(c.source_msgs) for c in D]
        print(f"{ws}: {calls} calls, {sum(len(v) for v in starts.values())} topic starts, "
              f"{len(D)} D chunks (avg {sum(sizes) / len(sizes):.1f} msgs) -> {seg_path(ws)}")


if __name__ == "__main__":
    main()
