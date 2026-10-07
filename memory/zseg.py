"""Chunker Z: zero-LLM-call topic segmentation (arm 1z of the 3-way comparison).

    python -m memory.zseg --ws ando | --all | --ws real   # -> data/cache/zsegments_<ws>.json + stats

TextTiling-style and strictly causal (unlike D, which sees up to 19 later messages): per channel,
message i starts a new segment when
  - it is the first message of the channel, or
  - the time gap to the previous channel message is > 2 h (real data: "ts"; simulated data has
    only "day", so a day change counts as a gap), or
  - its cosine similarity to the mean embedding of the previous 3 channel messages falls below
    mean - 1 std of all earlier such similarities in the channel (needs >= 5 earlier values),
    and the current segment already has >= 2 messages.
Embeddings: the same local MiniLM as the Threader ranker (memory.retrievers.THR_EMB), disk-cached.
Segments are then built by memory.segment.chunk_D, so Z and D differ ONLY in where boundaries
fall (same 12-message cap, same "[topic start]" header on split pieces). Chunk ids start "Z:".
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import numpy as np

from memory.base import load_msgs
from memory.retrievers import THR_EMB, embed
from memory.segment import _by_channel, chunk_D, load_segments

CACHE = Path("data/cache")
WINDOW, MIN_PREV, MIN_LEN, GAP_S = 3, 5, 2, 2 * 3600


def _gap(a: dict, b: dict) -> bool:
    if a.get("ts") and b.get("ts"):
        f = "%Y-%m-%dT%H:%M:%S"
        return (datetime.strptime(b["ts"][:19], f) - datetime.strptime(a["ts"][:19], f)).total_seconds() > GAP_S
    return a.get("day") != b.get("day")


def z_starts(msgs: list[dict]) -> dict:
    """channel -> [msg_ids that start a segment]."""
    out = {}
    for ch, ms in _by_channel(msgs).items():
        vecs = embed([m["text"] or "(empty)" for m in ms], "d", THR_EMB)
        starts, sims, cur = [ms[0]["msg_id"]], [], 1
        for i in range(1, len(ms)):
            prev = np.mean(vecs[max(0, i - WINDOW):i], axis=0)
            s = float(vecs[i] @ prev / (np.linalg.norm(prev) or 1.0))
            cut = _gap(ms[i - 1], ms[i])
            if not cut and len(sims) >= MIN_PREV and cur >= MIN_LEN:
                cut = s < np.mean(sims) - np.std(sims)
            sims.append(s)
            if cut:
                starts.append(ms[i]["msg_id"])
                cur = 1
            else:
                cur += 1
        out[ch] = starts
    return out


def zpath(ws: str) -> Path:
    return CACHE / f"zsegments_{ws}.json"


def chunk_Z(msgs: list[dict], ws: str | None = None):
    ws = ws or msgs[0]["msg_id"].split("/")[0]
    p = zpath(ws)
    starts = json.loads(p.read_text()) if p.exists() else z_starts(msgs)
    return [replace(c, chunk_id="Z" + c.chunk_id[1:]) for c in chunk_D(msgs, starts)]


def _avg_len(starts: dict, msgs) -> float:
    n = sum(len(ms) for ms in _by_channel(msgs).values())
    return n / max(sum(len(v) for v in starts.values()), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws")
    ap.add_argument("--all", action="store_true", help="the 4 simulated workspaces (never 'real')")
    a = ap.parse_args()
    from eval.costlog import log
    for ws in (["ando", "anthropic", "openai", "xai"] if a.all else [a.ws]):
        msgs = load_msgs(ws)
        t0 = time.perf_counter()
        st = z_starts(msgs)
        dt = time.perf_counter() - t0
        zpath(ws).write_text(json.dumps(st, indent=1))
        log("Z4", "segment", ws, seconds=dt, n_items=len(msgs), note="zero-call TextTiling (incl. embedding)")
        d = load_segments(ws)
        dl = f"{_avg_len(d, msgs):.1f}" if d else "n/a"
        print(f"{ws}: {len(msgs)} msgs, {sum(len(v) for v in st.values())} Z segments "
              f"(avg {_avg_len(st, msgs):.1f} msgs; D avg {dl}), {dt:.1f}s -> {zpath(ws)}")


if __name__ == "__main__":
    main()
