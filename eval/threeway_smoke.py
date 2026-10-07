"""Steps 3-4 smoke test: run the new conditions on real models before the full eval.

    uv run python -m eval.threeway_smoke            # ando plants + 20 real thread-root queries

For each condition: plant delivery (full evidence reached the agent at the 1,500-token budget) on
the 'ando' workspace's fact plants, hit rate on 20 real reference queries, retrieved tokens and
median ranking latency. Small n: this checks wiring and speed, it is NOT a result.
First run embeds everything with MiniLM (cached afterwards) and loads the reranker for *5 conditions.
"""
from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

from judge.conditions import parse
from memory.base import deliveries, fact_plants, load_msgs, load_plants, visible, window
from memory.build import build_chunks
from memory.retrievers import retrieve

CONDS = ["D1", "D4", "D5", "Z4", "L4", "L6", "E1", "E4"]


def run(ws, conds, queries):
    msgs = load_msgs(ws)
    by = {m["msg_id"]: m for m in msgs}
    built = {}
    out = {}
    for cond in conds:
        chunker, ranker = parse(cond)
        built.setdefault(chunker, build_chunks(ws, chunker, msgs))
        hits, toks, lat = [], [], []
        for q in queries:
            win = {m["msg_id"] for m in window(msgs, q["seq"], q["channel"])}
            vis = [c for c in visible(built[chunker], q["seq"], by) if not set(c.source_msgs) <= win]
            t0 = time.perf_counter()
            got = retrieve(vis, q["q"], ranker, 1500)
            lat.append(time.perf_counter() - t0)
            toks.append(sum(len(c.text) // 4 for c in got))
            hits.append(q["hit"](got, win))
        out[cond] = (sum(hits) / len(hits), statistics.mean(toks), statistics.median(lat) * 1000)
    return out


def main():
    msgs = load_msgs("ando")
    by = {m["msg_id"]: m for m in msgs}
    qs = []
    for p in fact_plants(load_plants("ando")):
        t = by.get(p.get("trigger_msg"))
        if not t:
            continue
        w = window(msgs, t["seq"], t["channel"])
        qs.append({"seq": t["seq"], "channel": t["channel"], "q": " \n".join(m["text"] for m in w[-3:]),
                   "hit": lambda got, win, p=p: deliveries(got, win, p)["all"] == "full"})
    print(f"ando: {len(qs)} plant queries (delivery = full evidence reached the agent)")
    for c, (h, tk, ms) in run("ando", CONDS, qs).items():
        print(f"  {c:<3} delivery {100*h:5.1f}%   ~{tk:5.0f} tokens   {ms:7.1f} ms/query")
    path = Path("data/real/ref_queries.jsonl")
    if path.exists():
        rq = [json.loads(l) for l in path.open()][:20]
        rq = [{**r, "q": r["query"], "hit": lambda got, win, t=set(r["target_msg_ids"]):
               any(t & set(c.source_msgs) for c in got)} for r in rq]
        print(f"real: {len(rq)} reference queries (hit = a target message is in retrieved memory)")
        for c, (h, tk, ms) in run("real", CONDS, rq).items():
            print(f"  {c:<3} hit      {100*h:5.1f}%   ~{tk:5.0f} tokens   {ms:7.1f} ms/query")


if __name__ == "__main__":
    main()
