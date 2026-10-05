"""Chunker E: write-time rewrite. Each message becomes 0-2 standalone statements.

    python -m memory.rewrite --ws ando | --all      # writes data/cache/rewrite_<ws>.jsonl

Context = previous 10 messages of the channel, plus the reply_to parent if it is older than that
(how a cross-thread "going with alex's idea" can be resolved). The model must say which messages
each statement depends on ("uses"); those become the chunk's source_msgs, so delivery is scored
against the original evidence. Statements are atomic: visible() drops them rather than cutting.

Plan deviation: uses parallel regular calls (disk-cached) instead of the Batch API; at Haiku
prices the difference is cents and results come back in minutes instead of up to 24 h.
"""
from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from memory.base import Chunk, load_msgs

REWRITE = """You keep a team's searchable memory. Recent messages in {CHANNEL}, oldest first:
{CONTEXT}
New message [{MSG_ID}]:
{MSG}
Rewrite the new message as 0-2 standalone statements a stranger could understand with no
other context. Resolve "I", "it", "that", "the idea from monday", emoji reactions and
corrections into explicit names, entities, values and dates. Keep only decisions, facts,
owners, dates, numbers, commitments and changes. If it carries none, return SKIP.
Return JSON only: {"statements": [{"text": "...", "uses": ["msg_ids it depends on"]}]}"""

CTX = 10
CACHE = Path("data/cache")


def _fmt(m):
    if m["kind"] == "reaction":
        return f"[{m['msg_id']}] ({m['day']}) {m['speaker']} reacted {m['text']} to [{m['reply_to']}]"
    return f"[{m['msg_id']}] ({m['day']}) {m['speaker']}: {m['text']}"


def rewrite_all(msgs: list[dict], workers: int = 8):
    from sim.llm import complete, parse_json
    model = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")
    by_id = {m["msg_id"]: m for m in msgs}
    hist, jobs = defaultdict(list), []
    for m in msgs:
        ctx = hist[m["channel"]][-CTX:]
        p = by_id.get(m["reply_to"]) if m["reply_to"] else None
        if p and p not in ctx:
            ctx = [p] + ctx
        jobs.append((m, ctx))
        hist[m["channel"]].append(m)

    def ask(job):
        m, ctx = job
        prompt = (REWRITE.replace("{CHANNEL}", m["channel"])
                  .replace("{CONTEXT}", "\n".join(_fmt(x) for x in ctx) or "(none)")
                  .replace("{MSG_ID}", m["msg_id"]).replace("{MSG}", _fmt(m)))
        r = complete(None, prompt, model=model, max_tokens=400)
        allowed = {x["msg_id"] for x in ctx} | {m["msg_id"]}
        stmts = []
        if "SKIP" not in r.text[:20]:
            try:
                for s in (parse_json(r.text).get("statements") or [])[:2]:
                    if s.get("text", "").strip():
                        uses = [u for u in s.get("uses", []) if u in allowed]
                        stmts.append({"text": s["text"].strip(), "uses": sorted(set(uses) | {m["msg_id"]})})
            except (ValueError, AttributeError, TypeError):
                pass
        return {"msg_id": m["msg_id"], "statements": stmts}

    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(ask, jobs))


def chunk_E(msgs: list[dict], rows: list[dict]) -> list[Chunk]:
    seq = {m["msg_id"]: m["seq"] for m in msgs}
    out = []
    for r in rows:
        for k, s in enumerate(r["statements"]):
            src = tuple(sorted(set(s["uses"]) | {r["msg_id"]}, key=seq.get))
            out.append(Chunk(f"E:{r['msg_id']}:{k}", src, seq[src[0]], seq[r["msg_id"]],
                             s["text"], atomic=True))
    return out


def rw_path(ws):
    return CACHE / f"rewrite_{ws}.jsonl"


def load_rewrite(ws):
    p = rw_path(ws)
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else None


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    for ws in (["ando", "anthropic", "openai", "xai"] if a.all else [a.ws]):
        msgs = load_msgs(ws)
        rows = rewrite_all(msgs, a.workers)
        CACHE.mkdir(parents=True, exist_ok=True)
        rw_path(ws).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        n = sum(len(r["statements"]) for r in rows)
        skipped = sum(not r["statements"] for r in rows)
        print(f"{ws}: {len(rows)} calls, {n} statements, {skipped} messages skipped -> {rw_path(ws)}")


if __name__ == "__main__":
    main()
