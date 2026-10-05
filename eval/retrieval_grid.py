"""Layers 1-2 for the whole grid, no judge spend: does the evidence reach the agent? (3.6)

    python -m eval.retrieval_grid --out results/retrieval_grid.csv [--budget 1500]

Queries
  plant        every fact plant; proactive (last 3 window msgs incl. the trigger) and reactive (probe)
  probe_trigger every row of probes/triggers.jsonl; proactive only (2 window msgs + the probe text)
Conditions
  chunker x retriever: A, B, C, Cstar, D, E  x  bm25, emb, rrf
  baselines: window (no memory; retriever "-") and oracle (evidence handed over; retriever "-")
Per row: chunks = visible(all chunks, q_seq) minus chunks whose sources are all in the window;
retrieve at the token budget; record delivery against all evidence groups and the origin group.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from memory.base import deliveries, fact_plants, load_msgs, load_plants, make_chunk, visible, window
from memory.build import CHUNKERS, build_chunks
from memory.retrievers import RANKERS, prefetch, retrieve
from sim.run_workspace import load

WSS = ["ando", "anthropic", "openai", "xai"]
COLS = ["ws", "query_id", "query_kind", "mode", "chunker", "retriever", "delivery", "origin_delivery",
        "evidence_form", "restated", "bucket", "structure", "n_chunks", "tokens"]


def queries(ws, msgs, by_id, d):
    struct = {t["id"]: t.get("structure", "flat") for t in d["threads"]}
    out = []
    for p in fact_plants(load_plants(ws)):
        trig = by_id[p["trigger_msg"]]
        win = window(msgs, trig["seq"], trig["channel"])
        base = {"query_id": p["plant_id"], "query_kind": "plant", "q_seq": trig["seq"], "plant": p,
                "win_ids": [m["msg_id"] for m in win], "evidence_form": p.get("evidence_form"),
                "restated": bool(p.get("restated")), "bucket": p.get("bucket"),
                "structure": p.get("structure") or struct.get(trig["thread"], "")}
        out.append(dict(base, mode="proactive", q=" \n".join(m["text"] for m in win[-3:])))
        out.append(dict(base, mode="reactive", q=p["probe"]))
    path = Path("probes/triggers.jsonl")
    if path.exists():
        for r in (json.loads(l) for l in path.read_text().splitlines()):
            if r["ws"] != ws:
                continue
            win = window(msgs, r["q_seq"] - 1, r["channel"], n=14)   # probe sits just before q_seq
            p = {"evidence_groups": r["evidence_groups"]}
            out.append({"query_id": r["probe_id"], "query_kind": "probe_trigger", "mode": "proactive",
                        "q_seq": r["q_seq"], "plant": p, "win_ids": [m["msg_id"] for m in win],
                        "q": " \n".join([m["text"] for m in win[-2:]] + [r["text"]]),
                        "evidence_form": r["origin_form"],
                        "restated": len(r["evidence_groups"]) > 1, "bucket": r["bucket"],
                        "structure": struct.get(r["thread"], "")})
    return out


def run(budget: int):
    rows = []
    for ws in WSS:
        msgs, d = load_msgs(ws), load(ws)
        by_id = {m["msg_id"]: m for m in msgs}
        qs = queries(ws, msgs, by_id, d)
        built = {c: build_chunks(ws, c, msgs) for c in CHUNKERS}
        # visible chunk sets per (query, chunker), then one batched embedding pass
        vis = {}
        for i, q in enumerate(qs):
            win = set(q["win_ids"])
            for c in CHUNKERS:
                vis[i, c] = [ch for ch in visible(built[c], q["q_seq"], by_id) if not set(ch.source_msgs) <= win]
        prefetch(list({ch.text for v in vis.values() for ch in v}), "d")
        prefetch(list({q["q"] for q in qs}), "q")
        print(f"{ws}: {len(qs)} queries, embeddings ready")

        for i, q in enumerate(qs):
            common = {k: q[k] for k in ("query_id", "query_kind", "mode", "evidence_form", "restated",
                                        "bucket", "structure")}
            dw = deliveries([], q["win_ids"], q["plant"])
            rows.append(dict(common, ws=ws, chunker="window", retriever="-", delivery=dw["all"],
                             origin_delivery=dw["origin"], n_chunks=0, tokens=0))
            orc = [make_chunk(f"O:{g['group']}", [by_id[m] for m in g["msgs"]])
                   for g in q["plant"]["evidence_groups"]]
            do = deliveries(visible(orc, q["q_seq"], by_id), q["win_ids"], q["plant"])
            rows.append(dict(common, ws=ws, chunker="oracle", retriever="-", delivery=do["all"],
                             origin_delivery=do["origin"], n_chunks=len(orc),
                             tokens=sum(len(c.text) // 4 for c in orc)))
            for c in CHUNKERS:
                for r in RANKERS:
                    got = retrieve(vis[i, c], q["q"], r, budget)
                    dl = deliveries(got, q["win_ids"], q["plant"])
                    rows.append(dict(common, ws=ws, chunker=c, retriever=r, delivery=dl["all"],
                                     origin_delivery=dl["origin"], n_chunks=len(got),
                                     tokens=sum(len(x.text) // 4 for x in got)))
    return rows


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/retrieval_grid.csv")
    ap.add_argument("--budget", type=int, default=1500)
    a = ap.parse_args()
    rows = run(a.budget)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in COLS})
    print(f"-> {a.out}: {len(rows)} rows", dict(Counter((r['query_kind'], r['mode']) for r in rows
                                                        if r['chunker'] == 'window')))


if __name__ == "__main__":
    main()
