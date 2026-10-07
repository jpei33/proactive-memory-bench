"""Arm 2 of the 3-way comparison: LLM-labeled conversational units (chunker "L").

    python -m memory.label_units --all | --ws real     # -> data/cache/labels_<ws>.json + cost rows

Inspired by Ando's public description of "conversational units"; NOT their implementation.
One cheap-model call per D chunk assigns 1-3 labels from a fixed set. Labels only, no summaries,
so this arm isolates write-time LABELING from write-time REWRITING (arm 3 = E).

Chunker L = the D chunks, each with "[labels: a, b]" prepended to its text, so BM25, the dense
views and the token budget all see the labels. Chunk ids start "L:". Causality: a chunk that
straddles the query point is rebuilt by memory.base.visible() from its raw messages (id + "~"),
which drops the label prefix, so labels computed on a whole segment never leak later messages.

Query-time use (memory.retrievers.rank_threader): if a chunk carries labels and the query's type
(keyword classifier, no LLM call) matches one, its score gets +gamma (0.15, fixed in advance).
Conditions: L4 = labels in text + boost (headline arm 2); L6 = labels in text, no boost (ablation).
"""
from __future__ import annotations

import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

from memory.base import load_msgs

LABELS = ["decision", "open_question", "commitment", "done", "blocker", "fyi"]
CACHE = Path("data/cache")
PROMPT = """You label segments of a team chat for a searchable memory.

Segment:
{TEXT}

Assign 1 to 3 labels that describe what happens in this segment, from this fixed set:
- decision: the team settles on a choice, plan, value or owner
- open_question: something is asked and is not answered within the segment
- commitment: someone says they will do something ("I'll take it", "on it", "will send by Friday")
- done: someone reports something finished ("shipped", "merged", "I did X", "fixed")
- blocker: something is stuck, waiting on someone, or cannot proceed
- fyi: information shared with no decision, question, commitment or status change

Reply with JSON only: {{"labels": ["...", "..."]}}"""
PREFIX = re.compile(r"^\[labels: ([a-z_, ]+)\]\n")


def lpath(ws: str) -> Path:
    return CACHE / f"labels_{ws}.json"


def label_chunks(ws: str, chunks, workers: int = 8) -> dict:
    from eval.costlog import log_result
    from sim.llm import complete, parse_json
    model = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")

    def one(c):
        r = complete(None, PROMPT.format(TEXT=c.text), model=model, max_tokens=60)
        log_result(r, arm="L4", stage="label", ws=ws, model=model)
        try:
            got = [l for l in parse_json(r.text).get("labels", []) if l in LABELS]
        except (ValueError, AttributeError):
            got = []
        return c.chunk_id, (list(dict.fromkeys(got))[:3] or ["fyi"])

    with ThreadPoolExecutor(workers) as ex:
        return dict(ex.map(one, chunks))


def load_labels(ws: str) -> dict | None:
    p = lpath(ws)
    return json.loads(p.read_text()) if p.exists() else None


def chunk_L(d_chunks, labels: dict):
    out = []
    for c in d_chunks:
        lab = labels.get(c.chunk_id) or ["fyi"]
        out.append(replace(c, chunk_id="L" + c.chunk_id[1:], text=f"[labels: {', '.join(lab)}]\n" + c.text))
    return out


def chunk_labels(c) -> list[str]:
    """Labels carried by a chunk's text ([] for unlabeled or visibility-truncated chunks)."""
    m = PREFIX.match(c.text)
    return [l.strip() for l in m.group(1).split(",")] if m else []


QTYPE = [  # (label, pattern) on the proactive query text; no LLM call at query time
    ("open_question", re.compile(r"\?")),
    ("commitment", re.compile(r"(?i)\b(i'?ll|i will|i can take|on it|will do|let me|i'?m taking)\b")),
    ("done", re.compile(r"(?i)\b(done|shipped|merged|fixed|finished|deployed|landed|completed|i did)\b")),
    ("decision", re.compile(r"(?i)\b(decided|decision|going with|we'?ll use|agreed|final|locked)\b")),
    ("blocker", re.compile(r"(?i)\b(blocked|blocking|waiting on|stuck|can'?t proceed)\b")),
]


def query_types(q: str) -> set[str]:
    return {lab for lab, pat in QTYPE if pat.search(q)}


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    from memory.build import build_chunks
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws")
    ap.add_argument("--all", action="store_true", help="the 4 simulated workspaces (never 'real')")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    from collections import Counter
    for ws in (["ando", "anthropic", "openai", "xai"] if a.all else [a.ws]):
        d = build_chunks(ws, "D", load_msgs(ws))
        labels = label_chunks(ws, d, a.workers)
        lpath(ws).write_text(json.dumps(labels, indent=1))
        dist = Counter(l for v in labels.values() for l in v)
        print(f"{ws}: {len(d)} D chunks labeled ({len(d)} calls) -> {lpath(ws)}")
        print("   ", ", ".join(f"{k} {v}" for k, v in dist.most_common()),
              f"| avg {sum(map(len, labels.values())) / max(len(labels), 1):.1f} labels/chunk")


if __name__ == "__main__":
    main()
