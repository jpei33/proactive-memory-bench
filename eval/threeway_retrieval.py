"""Step 7: retrieval effectiveness of the 3-way memory comparison, both datasets. No API calls.

    uv run python -m eval.threeway_retrieval            # all conditions incl. D5 on its subsets
    uv run python -m eval.threeway_retrieval --no-d5    # skip the slow reranker

Conditions (judge.conditions codes): D1 (D segments + BM25, reference), D4 (arm 1 Threader),
Z4 (arm 1z, zero-call segments), L4 (arm 2 labels + boost), L6 (labels, no boost),
E1 (arm 3 rewrite + BM25, your existing best), E4 (rewrite + Threader ranking).
D5 (D4 + bge reranker) runs only on the simulated plants (proactive) and the real queries.

Simulated (ground truth = ledger evidence groups), the same queries as eval/retrieval_grid.py:
  36 fact plants (proactive + reactive) and 155 probe triggers (proactive).
  delivery  = full evidence for the fact reached the agent within the 1,500-token budget (headline)
  mrr       = 1 / rank of the first chunk touching any evidence message (full ranking)
Real: data/real/ref_queries.jsonl. Headline set = thread_root (88); artifact (4) reported apart.
  hit       = a target message is in retrieved memory within the budget (headline)
  r@1/3/5, mrr by rank.
Also per query: retrieved tokens, ranking latency. Reranker latency is reported only over queries
where the reranker actually computed new scores (cache misses), so cached reruns don't look free.

CIs: 95% cluster bootstrap (simulated: over facts; real: over conversations). Paired differences
vs D4 and vs E1 on the same queries. Outputs:
  results/threeway_retrieval.csv            summary (no message text)
  results/threeway_retrieval_paired.csv     paired differences
  results/threeway_retrieval_sim_rows.csv   per query x condition, simulated
  data/real/threeway_retrieval_real_rows.csv per query x condition, real (git-ignored)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import memory.retrievers as R
from eval.retrieval_grid import queries as sim_queries
from judge.conditions import parse
from memory.base import deliveries, load_msgs, visible
from memory.build import build_chunks
from sim.run_workspace import load

SIM = ["ando", "anthropic", "openai", "xai"]
CONDS = ["D1", "D4", "Z4", "L4", "L6", "E1", "E4"]
BUDGET, B = 1500, 2000
RNG = np.random.default_rng(0)


def cut(chunks, order, budget=BUDGET):
    out, used = [], 0
    for i in order:
        n = len(chunks[i].text) // 4
        if used + n > budget:
            break
        out.append(chunks[i])
        used += n
    return out


def rank_of(chunks, order, targets: set) -> int | None:
    for r, i in enumerate(order, 1):
        if targets & set(chunks[i].source_msgs):
            return r
    return None


def rr_state():
    return R._rr[R.THR_RERANK].s.__len__() if R.THR_RERANK in R._rr else 0


def run_query(cond, chunks_vis, q):
    _, ranker = parse(cond)
    n0 = rr_state()
    t0 = time.perf_counter()
    order = R.ALL_RANKERS[ranker](chunks_vis, q)
    dt = time.perf_counter() - t0
    return order, dt, rr_state() - n0


def prefetch_ws(ws, built, qtexts):
    texts = []
    for chunks in built.values():
        for c in chunks:
            v, u = R._views_units(c)
            texts += [t for _, t in v] + u
    R.embed(list(dict.fromkeys(texts)), "d", R.THR_EMB)
    R.embed(list(dict.fromkeys(qtexts)), "q", R.THR_EMB)


def sim_rows(conds, d5):
    rows = []
    for ws in SIM:
        msgs, d = load_msgs(ws), load(ws)
        by = {m["msg_id"]: m for m in msgs}
        qs = sim_queries(ws, msgs, by, d)
        need = {parse(c)[0] for c in conds + (["D5"] if d5 else [])}
        built = {c: build_chunks(ws, c, msgs) for c in need}
        prefetch_ws(ws, built, [q["q"] for q in qs])
        print(f"{ws}: {len(qs)} queries", flush=True)
        for q in qs:
            win = set(q["win_ids"])
            ev = {m for g in q["plant"]["evidence_groups"] for m in g["msgs"]}
            p = q["plant"]
            cluster = (f"{ws}-{p.get('fact_id') or q['query_id']}" if q["query_kind"] == "plant"
                       else q["query_id"].split("@")[0])
            cl = conds + (["D5"] if d5 and q["query_kind"] == "plant" and q["mode"] == "proactive" else [])
            for cond in cl:
                ch = [c for c in visible(built[parse(cond)[0]], q["q_seq"], by) if not set(c.source_msgs) <= win]
                order, dt, new_rr = run_query(cond, ch, q["q"])
                got = cut(ch, order)
                rk = rank_of(ch, order, ev)
                rows.append({"ws": ws, "query_id": q["query_id"], "kind": q["query_kind"], "mode": q["mode"],
                             "cluster": cluster, "form": q["evidence_form"], "cond": cond,
                             "delivery_full": deliveries(got, q["win_ids"], q["plant"])["all"] == "full",
                             "mrr": 1 / rk if rk else 0.0, "tokens": sum(len(c.text) // 4 for c in got),
                             "n_chunks": len(got), "latency_ms": 1000 * dt, "rr_new": new_rr})
    return pd.DataFrame(rows)


def real_rows(conds, d5):
    path = Path("data/real/ref_queries.jsonl")
    if not path.exists():
        print("no data/real/ref_queries.jsonl: run python -m eval.ref_extract")
        return pd.DataFrame()
    qs = [json.loads(l) for l in path.open() if json.loads(l)["kind"] in ("thread_root", "artifact")]
    msgs = load_msgs("real")
    by = {m["msg_id"]: m for m in msgs}
    from memory.base import window
    allc = conds + (["D5"] if d5 else [])
    built = {c: build_chunks("real", c, msgs) for c in {parse(x)[0] for x in allc}}
    prefetch_ws("real", built, [q["query"] for q in qs])
    print(f"real: {len(qs)} queries", flush=True)
    rows = []
    for q in qs:
        win = {m["msg_id"] for m in window(msgs, q["seq"], q["channel"])}
        tg = set(q["target_msg_ids"])
        for cond in allc:
            ch = [c for c in visible(built[parse(cond)[0]], q["seq"], by) if not set(c.source_msgs) <= win]
            order, dt, new_rr = run_query(cond, ch, q["query"])
            got = cut(ch, order)
            rk = rank_of(ch, order, tg)
            rows.append({"query_id": q["qid"], "kind": q["kind"], "cluster": q["conversation"], "cond": cond,
                         "hit": any(tg & set(c.source_msgs) for c in got), "mrr": 1 / rk if rk else 0.0,
                         "r1": bool(rk and rk <= 1), "r3": bool(rk and rk <= 3), "r5": bool(rk and rk <= 5),
                         "tokens": sum(len(c.text) // 4 for c in got), "n_chunks": len(got),
                         "latency_ms": 1000 * dt, "rr_new": new_rr})
    return pd.DataFrame(rows)


def boot_mean(df, col, by="cluster"):
    g = df.groupby(by)[col].agg(["sum", "count"])
    s, n = g["sum"].values.astype(float), g["count"].values
    obs = s.sum() / n.sum()
    bs = [s[ix].sum() / n[ix].sum() for ix in (RNG.integers(0, len(s), len(s)) for _ in range(B))]
    return obs, *np.percentile(bs, [2.5, 97.5])


def boot_diff(df, col, a, b, by="cluster"):
    pv = df[df.cond.isin([a, b])].pivot_table(index=[by, "query_id"], columns="cond", values=col, aggfunc="first")
    if a not in pv or b not in pv:
        return None
    pv = pv.dropna()
    dd = (pv[a].astype(float) - pv[b].astype(float)).groupby(level=0).agg(["sum", "count"])
    s, n = dd["sum"].values, dd["count"].values
    obs = s.sum() / n.sum()
    bs = [s[ix].sum() / n[ix].sum() for ix in (RNG.integers(0, len(s), len(s)) for _ in range(B))]
    return obs, *np.percentile(bs, [2.5, 97.5]), int(n.sum())


def summarize(df, dataset, subset, metric, extra):
    out = []
    for cond, g in df.groupby("cond"):
        m, lo, hi = boot_mean(g, metric)
        cold = g[g.rr_new > 0].latency_ms
        row = {"dataset": dataset, "subset": subset, "cond": cond, "n": len(g), "metric": metric,
               "value": 100 * m, "lo": 100 * lo, "hi": 100 * hi, "mrr": g.mrr.mean(),
               "tokens": g.tokens.mean(), "empty_or_short": (g.tokens < 500).mean(),
               "latency_ms_median": g.latency_ms.median(),
               "latency_ms_median_cold": cold.median() if len(cold) else np.nan}
        for e in extra:
            row[e] = g[e].mean()
        out.append(row)
    return out


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-d5", action="store_true")
    ap.add_argument("--only", choices=["sim", "real"])
    a = ap.parse_args()
    d5 = not a.no_d5
    summ, paired = [], []
    if a.only != "real":
        sd = sim_rows(CONDS, d5)
        sd.to_csv("results/threeway_retrieval_sim_rows.csv", index=False)
        for subset, sub in [("all proactive (plants+triggers)", sd[sd["mode"] == "proactive"]),
                            ("plants proactive", sd[(sd.kind == "plant") & (sd["mode"] == "proactive")]),
                            ("plants reactive", sd[(sd.kind == "plant") & (sd["mode"] == "reactive")]),
                            ("probe triggers", sd[sd.kind == "probe_trigger"])]:
            summ += summarize(sub, "simulated", subset, "delivery_full", [])
            for ref in ("D4", "E1"):
                for c in sorted(sub.cond.unique()):
                    if c != ref and (r := boot_diff(sub, "delivery_full", c, ref)):
                        paired.append({"dataset": "simulated", "subset": subset, "cond": c, "ref": ref,
                                       "diff": 100 * r[0], "lo": 100 * r[1], "hi": 100 * r[2], "n": r[3]})
    if a.only != "sim":
        rd = real_rows(CONDS, d5)
        if len(rd):
            Path("data/real").mkdir(exist_ok=True)
            rd.to_csv("data/real/threeway_retrieval_real_rows.csv", index=False)
            for kind in ("thread_root", "artifact"):
                sub = rd[rd.kind == kind]
                if not len(sub):
                    continue
                summ += summarize(sub, "real", kind, "hit", ["r1", "r3", "r5"])
                if kind == "thread_root":
                    for ref in ("D4", "E1"):
                        for c in sorted(sub.cond.unique()):
                            if c != ref and (r := boot_diff(sub, "hit", c, ref)):
                                paired.append({"dataset": "real", "subset": kind, "cond": c, "ref": ref,
                                               "diff": 100 * r[0], "lo": 100 * r[1], "hi": 100 * r[2], "n": r[3]})
    R.save_caches()
    S, P = pd.DataFrame(summ), pd.DataFrame(paired)
    S.round(3).to_csv("results/threeway_retrieval.csv", index=False)
    P.round(2).to_csv("results/threeway_retrieval_paired.csv", index=False)
    order = {c: i for i, c in enumerate(["D1", "D4", "D5", "Z4", "L4", "L6", "E1", "E4"])}
    for (ds, subset), g in S.groupby(["dataset", "subset"], sort=False):
        g = g.sort_values("cond", key=lambda s: s.map(order))
        print(f"\n== {ds} | {subset} | {g.metric.iloc[0]} (95% CI) ==")
        for r in g.itertuples():
            ex = f"  r@1/3/5 {100*r.r1:4.0f}/{100*r.r3:3.0f}/{100*r.r5:3.0f}" if ds == "real" else ""
            cold = "" if np.isnan(r.latency_ms_median_cold) else f" (cold {r.latency_ms_median_cold:,.0f} ms)"
            print(f"  {r.cond:<3} {r.value:5.1f} [{r.lo:5.1f},{r.hi:5.1f}]  mrr {r.mrr:.2f}  n={r.n:<4}"
                  f"  ~{r.tokens:4.0f} tok  short {100*r.empty_or_short:3.0f}%  {r.latency_ms_median:7.1f} ms{cold}{ex}")
    if len(P):
        print("\n== paired differences (pts, 95% CI; * = excludes 0) ==")
        for r in P.itertuples():
            star = " *" if r.lo > 0 or r.hi < 0 else ""
            print(f"  {r.dataset:<9} {r.subset:<32} {r.cond:<3} - {r.ref}  {r.diff:+5.1f} [{r.lo:+5.1f},{r.hi:+5.1f}]{star}")
    print("\n-> results/threeway_retrieval.csv, results/threeway_retrieval_paired.csv")


if __name__ == "__main__":
    main()
