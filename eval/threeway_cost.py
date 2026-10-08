"""Step 9: cost vs. effectiveness of the 3 memory arms (run after eval/threeway_budget.py).

    python -m eval.threeway_cost       # -> results/threeway_cost.csv, results/threeway_cost.md,
                                       #    results/figs/threeway_cost.png   (no API calls, no spend)

Write-time LLM cost is rebuilt EXACTLY from the disk cache: the segmentation, labeling and rewrite
code is re-run with every request answered from data/cache/llm (a cache miss raises instead of
calling the API), and the token counts stored with each cached reply are summed. Prices:
eval/prices.json. Normalized per 100K chat messages and per 100K chat input tokens (Threader's
Table 4 unit).

  arm 1  (D4) Threader      = shared D segmentation (cheap model, ~1 call per 20 msgs per channel)
  arm 1z (Z4) zero-call     = 0 LLM calls (local MiniLM only)
  arm 2  (L4) labeled units = D segmentation + 1 call per segment
  arm 3  (E1) rewrite       = 1 call per message (does not need D)
  + D2 / B2 / L2: the same memories ranked with OpenAI text-embedding-3-large; they also pay to
    embed every chunk once at write time (chars/4 tokens x eval/prices.json; included in write_usd).

Query-time: every judge call pays for the context tokens memory hands over (judge = JUDGE_MODEL,
input price). From the budget sweep, the tokens each arm needs to match the retrieval E1 reaches at
1,500 tokens are interpolated (log-linear between sweep points). The extra tokens x judge input
price = extra $ per judge call; break-even = how many judge calls per message make E's one-time
write cost cheaper than paying for the larger context. A proactive agent makes a decision on
every incoming message, i.e. about 1 judge call per message.
Ranking latency (median ms per query, local) comes from results/threeway_retrieval.csv.
"""
from __future__ import annotations

import json
import os
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from eval.costlog import price
from memory.base import line, load_msgs

SIM = ["ando", "anthropic", "openai", "xai"]
DATASETS = {"simulated": SIM, "real": ["real"]}
ARMS = [("1", "D4", "Threader (raw segments, MiniLM)"), ("1z", "Z4", "Threader, zero-call segments"),
        ("1e", "D2", "Raw segments + 3-large embeddings"), ("1w", "B2", "Raw windows + 3-large (no LLM)"),
        ("2", "L4", "LLM-labeled units (MiniLM)"), ("2e", "L2", "LLM-labeled units + 3-large"),
        ("3", "E1", "Memory rewrite (BM25)")]
STAGES = {"D4": ["segment"], "Z4": [], "D2": ["segment"], "B2": [], "L4": ["segment", "label"],
          "L2": ["segment", "label"], "E1": ["rewrite"]}
EMB = {"D2": "D", "B2": "B", "L2": "L"}          # arms that pay an embedding API to index their chunks
EMB_MODEL = "text-embedding-3-large"


def embed_costs() -> pd.DataFrame:
    """Indexing cost of API embeddings: every chunk text embedded once (chars/4 tokens), per dataset.
    (Query embeddings, ~100 tokens per judge call, are ignored: < $0.00002 per call.)"""
    from memory.build import build_chunks
    prices = json.load(open("eval/prices.json"))
    rows = []
    for ds, wss in DATASETS.items():
        for cond, chunker in EMB.items():
            tok = sum(len(c.text) // 4 for ws in wss for c in build_chunks(ws, chunker, load_msgs(ws)))
            r = {"model": EMB_MODEL, "calls": 1, "in_tok": tok, "out_tok": 0, "cache_read_tok": 0}
            rows.append({"dataset": ds, "cond": cond, "emb_tokens": tok, "emb_usd": price(r, prices)})
    return pd.DataFrame(rows)


def write_costs() -> pd.DataFrame:
    """Exact write-time tokens per (dataset, stage), replayed from the LLM disk cache."""
    from dotenv import load_dotenv
    load_dotenv(".env")
    import sim.llm as L
    from memory.label_units import PROMPT as LPROMPT
    from memory.rewrite import rewrite_all
    from memory.segment import boundaries
    from memory.build import build_chunks

    def no_api(req):
        raise RuntimeError("cache miss: refusing to call the API while costing")
    L._call = no_api
    real_complete = L.complete
    acc = defaultdict(lambda: defaultdict(float))
    cur = {"key": None}

    def rec(*a, **k):
        r = real_complete(*a, **k)
        t = acc[cur["key"]]
        t["calls"] += 1
        t["in_tok"] += r.in_tok or 0
        t["out_tok"] += r.out_tok or 0
        t["cache_read_tok"] += r.cache_read_tok or 0
        t["model"] = k.get("model") or r.model
        return r
    L.complete = rec
    model = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")
    rows = []
    for ds, wss in DATASETS.items():
        n_msgs = n_tok = 0
        for ws in wss:
            msgs = load_msgs(ws)
            n_msgs += len(msgs)
            n_tok += sum(len(line(m)) // 4 for m in msgs)
            cur["key"] = (ds, "segment")
            boundaries(msgs)
            cur["key"] = (ds, "rewrite")
            rewrite_all(msgs)
            cur["key"] = (ds, "label")
            for c in build_chunks(ws, "D", msgs):
                rec(None, LPROMPT.format(TEXT=c.text), model=model, max_tokens=60)
        for st in ("segment", "label", "rewrite"):
            t = acc[(ds, st)]
            r = {"model": t["model"], "calls": t["calls"], "in_tok": t["in_tok"], "out_tok": t["out_tok"],
                 "cache_read_tok": t["cache_read_tok"]}
            rows.append({"dataset": ds, "stage": st, "messages": n_msgs, "chat_tokens": n_tok, **r,
                         "usd": price(r)})
    L.complete = real_complete
    return pd.DataFrame(rows)


def tokens_to_reach(curve: pd.DataFrame, target: float):
    """Log-linear interpolation of tokens_used at which retrieval first reaches target (None if never)."""
    c = curve.sort_values("tokens_used")
    xs, ys = np.log(c.tokens_used.clip(lower=1).values), c.value.values
    for i in range(len(ys)):
        if ys[i] >= target:
            if i == 0:
                return float(np.exp(xs[0]))
            f = (target - ys[i - 1]) / max(ys[i] - ys[i - 1], 1e-9)
            return float(np.exp(xs[i - 1] + f * (xs[i] - xs[i - 1])))
    return None


def main():
    prices = json.load(open("eval/prices.json"))
    judge = os.environ.get("JUDGE_MODEL") or "claude-sonnet-5-5"
    if not os.environ.get("JUDGE_MODEL"):
        from dotenv import load_dotenv
        load_dotenv(".env")
        judge = os.environ.get("JUDGE_MODEL", judge)
    jkey = next(k for k in prices if not k.startswith("_") and judge.startswith(k))
    j_in = prices[jkey]["in"] / 1e6                                   # $ per context token
    W = write_costs()
    EC = embed_costs()
    budget = pd.read_csv("results/threeway_budget.csv") if Path("results/threeway_budget.csv").exists() else None
    retr = pd.read_csv("results/threeway_retrieval.csv") if Path("results/threeway_retrieval.csv").exists() else None
    rows = []
    for ds in DATASETS:
        w = W[W.dataset == ds].set_index("stage")
        n_msgs, n_tok = int(w.messages.iloc[0]), int(w.chat_tokens.iloc[0])
        ref = None
        if budget is not None:
            b = budget[budget.dataset == ds]
            e15 = b[(b.cond == "E1") & (b.budget.astype(str) == "1500")]
            ref = float(e15.value.iloc[0]) if len(e15) else None
        for arm, cond, label in ARMS:
            calls = sum(w.loc[s, "calls"] for s in STAGES[cond])
            usd = sum(w.loc[s, "usd"] for s in STAGES[cond])
            ec = EC[(EC.dataset == ds) & (EC.cond == cond)]
            emb_usd = float(ec.emb_usd.iloc[0]) if len(ec) else 0.0
            usd += emb_usd
            row = {"dataset": ds, "arm": arm, "cond": cond, "label": label, "write_calls": calls,
                   "write_usd": usd, "of_which_embedding_usd": emb_usd, "write_calls_per_100k_msgs": 1e5 * calls / n_msgs,
                   "write_usd_per_100k_msgs": 1e5 * usd / n_msgs,
                   "write_usd_per_100k_chat_tokens": 1e5 * usd / n_tok, "write_usd_per_msg": usd / n_msgs}
            if budget is not None:
                b = budget[(budget.dataset == ds) & (budget.cond == cond)]
                at = b[b.budget.astype(str) == "1500"]
                row["retrieval_at_1500"] = float(at.value.iloc[0]) if len(at) else np.nan
                row["retrieval_ci"] = f"[{at.lo.iloc[0]:.0f}, {at.hi.iloc[0]:.0f}]" if len(at) else ""
                row["retrieval_all_memory"] = float(b[b.budget.astype(str) == "all"].value.iloc[0]) if len(b) else np.nan
                need = tokens_to_reach(b[b.budget.astype(str) != "all"], ref) if ref is not None and len(b) else None
                row["tokens_to_match_E1@1500"] = need
                at15 = float(at.tokens_used.iloc[0]) if len(at) else np.nan
                row["tokens_used_at_1500"] = at15
                extra = (need - at15) if need else np.nan
                # within ~2% / 25 tokens of what it already uses = no extra context needed: no break-even
                row["extra_judge_usd_per_call"] = (extra * j_in if extra == extra and extra > max(25, 0.02 * at15)
                                                   else np.nan)
            if retr is not None:
                sub = "all proactive (plants+triggers)" if ds == "simulated" else "thread_root"
                r = retr[(retr.dataset == ds) & (retr.subset == sub) & (retr.cond == cond)]
                row["latency_ms_per_query"] = float(r.latency_ms_median.iloc[0]) if len(r) else np.nan
            rows.append(row)
    C = pd.DataFrame(rows)
    # break-even: E's write cost minus the arm's own write cost, vs the arm's extra judge $ per call
    if "extra_judge_usd_per_call" in C:
        e = C[C.cond == "E1"].set_index("dataset").write_usd_per_msg
        C["breakeven_judge_calls_per_msg"] = [
            (e[r.dataset] - r.write_usd_per_msg) / r.extra_judge_usd_per_call
            if r.cond != "E1" and r.extra_judge_usd_per_call and r.extra_judge_usd_per_call > 0 else np.nan
            for r in C.itertuples()]
    C.round(6).to_csv("results/threeway_cost.csv", index=False)
    W.round(6).to_csv("results/threeway_write_costs.csv", index=False)

    print("== write-time LLM usage, replayed from the cache ==")
    print(W[["dataset", "stage", "messages", "calls", "in_tok", "out_tok", "usd"]].round(4).to_string(index=False))
    print(f"\njudge input price: ${j_in * 1e6:.2f}/M tokens ({judge})")
    for ds in DATASETS:
        print(f"\n== {ds} ==")
        for r in C[C.dataset == ds].itertuples():
            print(f"arm {r.arm:<2} {r.cond}  write: {r.write_calls_per_100k_msgs:8,.0f} calls  "
                  f"${r.write_usd_per_100k_msgs:8.2f} per 100K msgs")
        if "retrieval_at_1500" in C:
            for r in C[C.dataset == ds].to_dict("records"):
                need = r.get("tokens_to_match_E1@1500")
                ns = "never (even all memory)" if (need is None or (isinstance(need, float) and np.isnan(need))) else f"{need:,.0f} tok"
                be = r.get("breakeven_judge_calls_per_msg")
                bes = "" if be is None or np.isnan(be) else f" | E pays off above {be:.2f} judge calls/msg"
                print(f"   {r['cond']}: retrieval@1500 {r['retrieval_at_1500']:5.1f}% {r['retrieval_ci']}  "
                      f"all-memory {r['retrieval_all_memory']:5.1f}%  tokens to match E1@1500: {ns}{bes}  "
                      f"latency {r.get('latency_ms_per_query', float('nan')):.0f} ms")
    plot(C)
    write_md(C, W, j_in, judge)
    print("\n-> results/threeway_cost.csv, results/threeway_cost.md, results/figs/threeway_cost.png")


def plot(C):
    if "retrieval_at_1500" not in C:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    col = {"D4": "#2a78d6", "Z4": "#1baf7a", "L4": "#eda100", "E1": "#eb6834", "D2": "#4a3aa7",
           "B2": "#008300", "L2": "#e34948"}
    name = {"Z4": "Z4 zero-call", "B2": "B2 windows+3-large", "D4": "D4 Threader", "D2": "D2 segments+3-large",
            "L4": "L4 labels", "L2": "L2 labels+3-large", "E1": "E1 rewrite"}
    # label placement (dx pts, dy pts, ha): neighbours on the x axis go to opposite sides
    place = {"Z4": (9, 0, "left"), "B2": (9, 0, "left"), "D4": (-9, -4, "right"), "D2": (-9, 4, "right"),
             "L4": (9, -4, "left"), "L2": (9, 4, "left"), "E1": (-9, 0, "right")}
    place_real = {"B2": (9, -12, "left"), "D4": (-9, -10, "right"), "D2": (-9, 8, "right"),
                  "L4": (-9, -10, "right"), "L2": (9, 6, "left"), "E1": (9, 0, "left")}
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": grid, "axes.labelcolor": ink2, "xtick.color": ink2,
                         "ytick.color": ink2, "figure.facecolor": surf, "axes.facecolor": surf})
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), sharey=True)
    floor = 0.1
    for ax, ds in zip(axes, ("simulated", "real")):
        for r in C[C.dataset == ds].itertuples():
            x = max(r.write_usd_per_100k_msgs, floor)
            lo, hi = [float(v) for v in r.retrieval_ci.strip("[]").split(",")]
            ax.errorbar(x, r.retrieval_at_1500, yerr=[[r.retrieval_at_1500 - lo], [hi - r.retrieval_at_1500]],
                        fmt="o", ms=9, color=col[r.cond], mec=surf, mew=1.5, elinewidth=1.2, capsize=0,
                        alpha=0.95, zorder=3, label=name.get(r.cond, r.cond) if ds == "simulated" else None)
            pass
        ax.text(floor, 3, r"  \$0 shown at \$0.10", fontsize=8, color=ink2)
        ax.set_xscale("log")
        ax.set_xlim(0.06, 400)
        ax.set_xlabel("write-time cost, $ per 100K messages (LLM calls + embeddings; log scale)")
        ax.set_title(f"{ds}: {'191 proactive queries' if ds == 'simulated' else '88 thread-root queries'}",
                     loc="left", fontsize=11, fontweight="bold", color=ink)
        ax.grid(True, color=grid, lw=0.8)
        ax.set_ylim(0, 100)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("retrieval at 1,500 context tokens (%)")
    h, l = axes[0].get_legend_handles_labels()
    order = ["Z4 zero-call", "B2 windows+3-large", "D4 Threader", "D2 segments+3-large", "L4 labels",
             "L2 labels+3-large", "E1 rewrite"]
    hl = sorted(zip(h, l), key=lambda t: order.index(t[1]) if t[1] in order else 99)
    fig.legend([x for x, _ in hl], [y for _, y in hl], frameon=False, loc="lower center", ncol=7, fontsize=9,
               labelcolor=ink2, handletextpad=0.3, columnspacing=1.2)
    fig.suptitle("Retrieval vs. write-time cost (bars = 95% CI)", x=0.01, ha="left", fontsize=12, color=ink)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig("results/figs/threeway_cost.png", dpi=170)


def md_table(df: pd.DataFrame) -> str:
    """Markdown table without the optional 'tabulate' dependency."""
    def f(v):
        if isinstance(v, float):
            return "" if np.isnan(v) else f"{v:,.3f}".rstrip("0").rstrip(".")
        return str(v)
    head = "| " + " | ".join(map(str, df.columns)) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    return "\n".join([head, sep] + ["| " + " | ".join(f(v) for v in r) + " |" for r in df.itertuples(index=False)])


def write_md(C, W, j_in, judge):
    L = ["# 3-way memory comparison: cost vs. effectiveness", "",
         "Generated by `eval/threeway_cost.py`. Write-time costs replayed exactly from the LLM cache; "
         f"query-time context priced at the judge's input rate (${j_in * 1e6:.2f}/M, {judge}).", ""]
    cols = ["arm", "cond", "label", "write_calls_per_100k_msgs", "write_usd_per_100k_msgs",
            "write_usd_per_100k_chat_tokens", "retrieval_at_1500", "retrieval_ci", "retrieval_all_memory",
            "tokens_to_match_E1@1500", "breakeven_judge_calls_per_msg", "latency_ms_per_query"]
    for ds in DATASETS:
        g = C[C.dataset == ds][[c for c in cols if c in C]]
        L += [f"## {ds}", "", md_table(g.round(3)), ""]
    L += ["## Write-time usage (cache replay)", "", md_table(W.round(4)), ""]
    Path("results/threeway_cost.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
