"""Infer reply parents the way a real system could: Slack-visible links first, then Haiku.

    python -m memory.linker --ws ando          # writes data/cache/parents_ando.json
    python -m memory.linker --all

Visible for free: reaction targets and thread replies (thread_ts). Everything else, i.e. plain
channel messages, gets one Haiku call: "which earlier message is this replying to?" over the last
12 messages of the channel. Calls are independent, so they run in parallel; output is cached so the
grid run never re-calls it.
"""
from __future__ import annotations

import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from memory.base import load_msgs

LINK = """Messages from one team chat channel, oldest first:
{NUMBERED}
Which earlier message is message [{N}] replying to or answering?
Consider @mentions, who asked what, and short answers like "me", "on it", "yep".
Answer with the number only, or NONE if it starts something new."""

CACHE = Path("data/cache")
HIST = 12


def _prompt(recent: list[dict], m: dict) -> str:
    numbered = "\n".join(f"[{i}] {x['speaker']}: {x['text']}" for i, x in enumerate(recent + [m]))
    return LINK.replace("{NUMBERED}", numbered).replace("{N}", str(len(recent)))


def infer_parents(msgs: list[dict], workers: int = 8) -> tuple[dict, dict]:
    """Returns (parent map, stats). Uses sim.llm.complete (disk-cached) with the cheap model."""
    from sim.llm import complete
    model = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")
    parent, jobs, by_ch = {}, [], {}
    for m in msgs:                                   # seq order
        hist = by_ch.setdefault(m["channel"], [])
        if m["kind"] == "reaction":
            parent[m["msg_id"]] = m["reply_to"]      # Slack shows reaction targets
        elif m["thread_ts"]:
            parent[m["msg_id"]] = m["reply_to"]      # visible thread reply
        elif not hist:
            parent[m["msg_id"]] = None
        else:
            jobs.append((m, hist[-HIST:]))
        hist.append(m)

    def ask(job):
        m, recent = job
        r = complete(None, _prompt(recent, m), model=model, max_tokens=5)
        k = r.text.strip().strip("[].")
        return m["msg_id"], (recent[int(k)]["msg_id"] if k.isdigit() and int(k) < len(recent) else None), r.cached

    cached = 0
    with ThreadPoolExecutor(workers) as ex:
        for mid, p, was_cached in ex.map(ask, jobs):
            parent[mid] = p
            cached += was_cached
    return parent, {"messages": len(msgs), "llm_calls": len(jobs), "from_cache": cached,
                    "free_links": len(msgs) - len(jobs)}


def parents_path(ws: str) -> Path:
    return CACHE / f"parents_{ws}.json"


def load_parents(ws: str) -> dict | None:
    p = parents_path(ws)
    return json.loads(p.read_text()) if p.exists() else None


def link_accuracy(msgs: list[dict], parent: dict) -> dict:
    """How often inferred parents match the simulator's true reply_to (on non-free links)."""
    rows = [m for m in msgs if m["kind"] == "message" and not m["thread_ts"]]
    has = [m for m in rows if m["reply_to"]]
    none = [m for m in rows if not m["reply_to"]]
    return {"linked_msgs_correct": f"{sum(parent.get(m['msg_id']) == m['reply_to'] for m in has)}/{len(has)}",
            "unlinked_msgs_correct": f"{sum(parent.get(m['msg_id']) is None for m in none)}/{len(none)}"}


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    wss = ["ando", "anthropic", "openai", "xai"] if a.all else [a.ws]
    for ws in wss:
        msgs = load_msgs(ws)
        parent, stats = infer_parents(msgs, a.workers)
        CACHE.mkdir(parents=True, exist_ok=True)
        parents_path(ws).write_text(json.dumps(parent, indent=0))
        print(f"{ws}: {stats} | accuracy vs gold {link_accuracy(msgs, parent)} -> {parents_path(ws)}")


if __name__ == "__main__":
    main()
