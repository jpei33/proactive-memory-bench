"""Budget sweep for the 3-way comparison: retrieval vs. context tokens handed to the judge.

    uv run python -m eval.threeway_budget        # -> results/threeway_budget.csv + figs/threeway_budget.png

Step 7 compared arms at one budget (1,500 tokens). There, rewrite memory (E) won on simulated data
largely by BREADTH: ~43 short statements fit where ~6 raw segments do. The fair cost question is
therefore how many context tokens each arm needs for the same retrieval, because context tokens
are paid on every judge call while E's rewrite is paid once at write time (eval/threeway_cost.py
turns this into $).

Conditions ending in 2 use OpenAI text-embedding-3-large (EMBED_MODEL default), prefetched in one
batched pass; D2/B2 = raw memory with a strong embedder, L2 = labeled units with it.
Each query is ranked ONCE per condition; the same ranking is then cut at every budget, so the
sweep costs about one Step-7 pass. Budgets: 250 ... 6,000 tokens and "all" (everything visible).
Queries and metrics are those of eval/threeway_retrieval.py (simulated: proactive plants + probe
triggers, full-evidence delivery; real: thread-root hit). CIs: cluster bootstrap as in Step 7.
tokens_used = what was actually handed over (can be below the budget when memory runs out).
No API calls; needs the local MiniLM model (cached embeddings from Step 7 are reused).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import memory.retrievers as R
from eval.retrieval_grid import queries as sim_queries
from eval.threeway_retrieval import boot_mean, cut, prefetch_ws
from judge.conditions import parse
from memory.base import deliveries, load_msgs, visible, window
from memory.build import build_chunks
from sim.run_workspace import load

SIM = ["ando", "anthropic", "openai", "xai"]
CONDS = ["D1", "D2", "B2", "D4", "Z4", "L4", "L2", "E1", "E4"]   # *2 = OpenAI text-embedding-3-large
BUDGETS = [250, 500, 1000, 1500, 3000, 6000, None]          # None = everything visible


def prefetch_emb(ws, built, qs, vis_of):
    """OpenAI embeddings (conditions with retriever 2) for every visible chunk text and query, batched."""
    need = [c for c in CONDS if parse(c)[1] == "emb"]
    if not need:
        return
    texts = {ch.text for c in need for q in qs for ch in vis_of(built[parse(c)[0]], q)}
    R.prefetch(sorted(texts), "d")
    R.prefetch(sorted({q.get("q") or q.get("query") for q in qs}), "q")


def sweep_sim():
    rows = []
    for ws in SIM:
        msgs, d = load_msgs(ws), load(ws)
        by = {m["msg_id"]: m for m in msgs}
        qs = [q for q in sim_queries(ws, msgs, by, d) if q["mode"] == "proactive"]
        built = {c: build_chunks(ws, c, msgs) for c in {parse(x)[0] for x in CONDS}}
        prefetch_ws(ws, built, [q["q"] for q in qs])
        prefetch_emb(ws, built, qs, lambda chunks, q: [c for c in visible(chunks, q["q_seq"], by)
                                                      if not set(c.source_msgs) <= set(q["win_ids"])])
        print(f"{ws}: {len(qs)} queries", flush=True)
        for q in qs:
            win = set(q["win_ids"])
            p = q["plant"]
            cluster = (f"{ws}-{p.get('fact_id') or q['query_id']}" if q["query_kind"] == "plant"
                       else q["query_id"].split("@")[0])
            for cond in CONDS:
                ch = [c for c in visible(built[parse(cond)[0]], q["q_seq"], by) if not set(c.source_msgs) <= win]
                order = R.ALL_RANKERS[parse(cond)[1]](ch, q["q"])
                for b in BUDGETS:
                    got = cut(ch, order, b if b else 10 ** 9)
                    rows.append({"dataset": "simulated", "query_id": q["query_id"], "cluster": cluster,
                                 "cond": cond, "budget": b or "all",
                                 "ok": deliveries(got, q["win_ids"], p)["all"] == "full",
                                 "tokens_used": sum(len(c.text) // 4 for c in got)})
    return rows


def sweep_real():
    path = Path("data/real/ref_queries.jsonl")
    qs = [json.loads(l) for l in path.open()] if path.exists() else []
    qs = [q for q in qs if q["kind"] == "thread_root"]
    if not qs:
        return []
    msgs = load_msgs("real")
    by = {m["msg_id"]: m for m in msgs}
    built = {c: build_chunks("real", c, msgs) for c in {parse(x)[0] for x in CONDS}}
    prefetch_ws("real", built, [q["query"] for q in qs])
    wins = {q["qid"]: {m["msg_id"] for m in window(msgs, q["seq"], q["channel"])} for q in qs}
    prefetch_emb("real", built, qs, lambda chunks, q: [c for c in visible(chunks, q["seq"], by)
                                                      if not set(c.source_msgs) <= wins[q["qid"]]])
    print(f"real: {len(qs)} thread-root queries", flush=True)
    rows = []
    for q in qs:
        win = {m["msg_id"] for m in window(msgs, q["seq"], q["channel"])}
        tg = set(q["target_msg_ids"])
        for cond in CONDS:
            ch = [c for c in visible(built[parse(cond)[0]], q["seq"], by) if not set(c.source_msgs) <= win]
            order = R.ALL_RANKERS[parse(cond)[1]](ch, q["query"])
            for b in BUDGETS:
                got = cut(ch, order, b if b else 10 ** 9)
                rows.append({"dataset": "real", "query_id": q["qid"], "cluster": q["conversation"],
                             "cond": cond, "budget": b or "all",
                             "ok": any(tg & set(c.source_msgs) for c in got),
                             "tokens_used": sum(len(c.text) // 4 for c in got)})
    return rows


def plot(S):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    col = {"D4": "#2a78d6", "Z4": "#1baf7a", "L4": "#eda100", "E1": "#eb6834", "D1": "#52514e", "E4": "#e87ba4",
           "D2": "#4a3aa7", "B2": "#008300", "L2": "#e34948"}
    name = {"D4": "D4 · Threader (arm 1)", "Z4": "Z4 · Threader, 0 LLM calls (1z)",
            "L4": "L4 · labeled units (arm 2)", "E1": "E1 · rewrite + BM25 (arm 3)",
            "D1": "D1 · segments + BM25", "E4": "E4 · rewrite + Threader rank",
            "D2": "D2 · segments + 3-large embeddings", "B2": "B2 · windows + 3-large (no LLM)",
            "L2": "L2 · labeled units + 3-large"}
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": grid, "axes.labelcolor": ink2, "xtick.color": ink2,
                         "ytick.color": ink2, "figure.facecolor": surf, "axes.facecolor": surf})
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.9), sharey=True)
    for ax, ds, ylab in zip(axes, ["simulated", "real"],
                            ["retrieval (%): full evidence / target reached", None]):
        g = S[(S.dataset == ds) & (S.budget != "all")].copy()
        if g.empty:
            ax.set_visible(False)
            continue
        g["b"] = g.budget.astype(int)
        for cond in ["D1", "E4", "L4", "L2", "B2", "Z4", "D4", "D2", "E1"]:
            h = g[g.cond == cond].sort_values("b")
            if h.empty:
                continue
            main = cond in ("D4", "E1", "Z4", "D2")
            ax.plot(h.tokens_used, h.value, "-o", color=col[cond], lw=2 if main else 1.2, ms=5 if main else 3,
                    alpha=1 if main else 0.6, label=name[cond], zorder=3 if main else 2)
            if main:
                ax.fill_between(h.tokens_used, h.lo, h.hi, color=col[cond], alpha=0.12, lw=0)
        ax.axvline(1500, color=ink2, lw=1, ls=":")
        ax.text(1500, 96, " Step-7 budget", color=ink2, fontsize=8, va="top")
        ax.set_xscale("log")
        ax.set_xlabel("context tokens handed to the judge (mean, log scale)")
        if ylab:
            ax.set_ylabel(ylab)
        ax.set_title(f"{ds}: {'191 proactive queries' if ds == 'simulated' else '88 thread-root queries'}",
                     loc="left", fontsize=11, fontweight="bold", color=ink)
        ax.grid(True, color=grid, lw=0.8)
        ax.set_ylim(0, 102)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=9, loc="lower center", ncol=3, labelcolor=ink2)  # 9 entries -> 3 rows
    fig.suptitle("Retrieval vs. context budget (shaded = 95% CI for D4, Z4, D2, E1)", x=0.01, ha="left",
                 fontsize=12, color=ink)
    fig.tight_layout(rect=(0, 0.15, 1, 1))
    Path("results/figs").mkdir(parents=True, exist_ok=True)
    fig.savefig("results/figs/threeway_budget.png", dpi=170)


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    rows = sweep_sim() + sweep_real()
    df = pd.DataFrame(rows)
    df[df.dataset == "simulated"].to_csv("results/threeway_budget_sim_rows.csv", index=False)
    if (df.dataset == "real").any():
        df[df.dataset == "real"].to_csv("data/real/threeway_budget_real_rows.csv", index=False)
    out = []
    for (ds, cond, b), g in df.groupby(["dataset", "cond", "budget"], sort=False):
        m, lo, hi = boot_mean(g, "ok")
        out.append({"dataset": ds, "cond": cond, "budget": b, "n": len(g), "value": 100 * m, "lo": 100 * lo,
                    "hi": 100 * hi, "tokens_used": g.tokens_used.mean()})
    S = pd.DataFrame(out)
    S.round(2).to_csv("results/threeway_budget.csv", index=False)
    for ds in ("simulated", "real"):
        g = S[S.dataset == ds]
        if g.empty:
            continue
        print(f"\n== {ds}: retrieval % at each budget (mean tokens actually used) ==")
        pv = g.pivot_table(index="cond", columns="budget", values="value", aggfunc="first")
        tk = g.pivot_table(index="cond", columns="budget", values="tokens_used", aggfunc="first")
        cols = [b for b in BUDGETS if (b or "all") in pv.columns]
        print("cond  " + "".join(f"{str(b or 'all'):>13}" for b in cols))
        for c in CONDS:
            if c in pv.index:
                print(f"{c:<5} " + "".join(f"{pv.loc[c, b or 'all']:6.1f} ({tk.loc[c, b or 'all']:4.0f})" for b in cols))
    plot(S)
    print("\n-> results/threeway_budget.csv, results/figs/threeway_budget.png")


if __name__ == "__main__":
    main()
