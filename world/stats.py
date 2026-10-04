"""Corpus statistics for all generated workspaces.

    python -m world.stats                 # prints and writes results/corpus_stats.txt
    python -m world.stats --ws ando,xai   # subset

Tables: messages per workspace; plants by type / bucket / evidence form / restated /
structure; form x bucket for INTERVENE fact plants; decoys by type.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ALL = ["ando", "anthropic", "openai", "xai"]
FORMS = ["explicit", "ellipsis", "reaction", "correction", "cross_ref", "distributed"]
BUCKETS = ["near", "far", "cross"]


def table(title, rows, cols, out):
    """rows: list of (label, dict). Prints a fixed-width table with a total row."""
    w0 = max([len(title)] + [len(str(r[0])) for r in rows] + [5])
    ws = [max(len(c), 5) for c in cols]
    out.append(f"{title:<{w0}}  " + "  ".join(f"{c:>{w}}" for c, w in zip(cols, ws)) + f"  {'total':>5}")
    tot = Counter()
    for label, counts in rows:
        tot.update(counts)
        out.append(f"{label:<{w0}}  " + "  ".join(f"{counts.get(c, 0):>{w}}" for c, w in zip(cols, ws))
                   + f"  {sum(counts.get(c, 0) for c in cols):>5}")
    if len(rows) > 1:
        out.append(f"{'TOTAL':<{w0}}  " + "  ".join(f"{tot.get(c, 0):>{w}}" for c, w in zip(cols, ws))
                   + f"  {sum(tot.get(c, 0) for c in cols):>5}")
    out.append("")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", default=",".join(ALL))
    ap.add_argument("--out", default="results/corpus_stats.txt")
    a = ap.parse_args()
    names = a.ws.split(",")
    data = {}
    for ws in names:
        base = Path(f"data/workspaces/{ws}")
        data[ws] = ([json.loads(l) for l in (base / "messages.jsonl").read_text().splitlines()],
                    [json.loads(l) for l in (base / "plants.jsonl").read_text().splitlines()])

    out = ["Corpus statistics", "=================", ""]

    # messages
    out.append(f"{'messages':<10}  {'total':>5}  {'main':>5}  {'side':>5}  {'react':>5}  "
               f"{'reply_to':>8}  {'threaded':>8}  {'threads':>7}  {'avg words':>9}")
    T = Counter()
    for ws, (msgs, _) in data.items():
        main = [m for m in msgs if not m["side"]]
        r = Counter(total=len(msgs), main=len(main), side=len(msgs) - len(main),
                    react=sum(m["kind"] == "reaction" for m in msgs),
                    reply=sum(bool(m["reply_to"]) for m in msgs),
                    thr=sum(bool(m["thread_ts"]) for m in msgs),
                    threads=len({m["thread"] for m in msgs}),
                    words=sum(len(m["text"].split()) for m in msgs if m["kind"] == "message"))
        T.update(r)
        out.append(f"{ws:<10}  {r['total']:>5}  {r['main']:>5}  {r['side']:>5}  {r['react']:>5}  "
                   f"{r['reply'] / r['total']:>8.0%}  {r['thr'] / r['total']:>8.0%}  {r['threads']:>7}  "
                   f"{r['words'] / max(1, r['total'] - r['react']):>9.1f}")
    out.append(f"{'TOTAL':<10}  {T['total']:>5}  {T['main']:>5}  {T['side']:>5}  {T['react']:>5}  "
               f"{T['reply'] / T['total']:>8.0%}  {T['thr'] / T['total']:>8.0%}  {T['threads']:>7}  "
               f"{T['words'] / max(1, T['total'] - T['react']):>9.1f}")
    out.append("")

    plants = {ws: [p for p in ps if p["kind"] == "plant"] for ws, (_, ps) in data.items()}
    decoys = {ws: [p for p in ps if p["kind"] == "decoy"] for ws, (_, ps) in data.items()}

    table("plants by label", [(ws, Counter(p["gold_label"] for p in ps)) for ws, ps in plants.items()],
          ["INTERVENE", "TRACK"], out)
    types = sorted({p["type"] for ps in plants.values() for p in ps})
    table("plants by type", [(ws, Counter(p["type"] for p in ps)) for ws, ps in plants.items()], types, out)

    iv = {ws: [p for p in ps if p["gold_label"] == "INTERVENE"] for ws, ps in plants.items()}
    table("INTERVENE plants by bucket", [(ws, Counter(p.get("bucket") for p in ps)) for ws, ps in iv.items()],
          BUCKETS, out)

    fact = {ws: [p for p in ps if p.get("fact_id")] for ws, ps in iv.items()}
    table("INTERVENE fact plants by evidence form",
          [(ws, Counter(p.get("evidence_form") for p in ps)) for ws, ps in fact.items()], FORMS, out)
    table("... of which not restated (clean)",
          [(ws, Counter(p.get("evidence_form") for p in ps if not p.get("restated"))) for ws, ps in fact.items()],
          FORMS, out)

    allfact = [p for ps in fact.values() for p in ps]
    table("form x bucket (all workspaces)",
          [(f, Counter(p.get("bucket") for p in allfact if p.get("evidence_form") == f)) for f in FORMS],
          BUCKETS, out)
    table("form x origin structure (all workspaces)",
          [(f, Counter(p.get("structure") for p in allfact if p.get("evidence_form") == f)) for f in FORMS],
          ["threaded", "flat", "interleaved"], out)

    item = [p for ps in iv.values() for p in ps if p.get("item_id")]
    out.append(f"deadline_passed plants (evidence = an explicit commitment): {len(item)}")
    dist = sorted(p["distance_msgs"] for p in allfact + item if "distance_msgs" in p)
    if dist:
        out.append(f"evidence distance in messages: min {dist[0]}, median {dist[len(dist) // 2]}, max {dist[-1]}")
    out.append("")

    dtypes = sorted({p["type"] for ps in decoys.values() for p in ps})
    table("decoys by type", [(ws, Counter(p["type"] for p in ps)) for ws, ps in decoys.items()], dtypes, out)

    text = "\n".join(out)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(text + "\n")
    print(text)
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
