"""Do the rankings hold with a different judge and a different embedding model? (5.3)

    python -m eval.robustness       # -> results/robustness.csv + a one-line verdict per check

Needs, from the runs:
  judge:     <cond>~haiku_b1500.jsonl next to <cond>_b1500.jsonl (scored into results/main.csv by eval.score)
  embedding: results/retrieval_grid_minilm.csv (same grid, EMBED_MODEL=local:...MiniLM)
Spearman rho is computed across the conditions both versions have.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def rho(a: pd.Series, b: pd.Series):
    j = pd.concat([a, b], axis=1).dropna()
    return (round(j.iloc[:, 0].corr(j.iloc[:, 1], method="spearman"), 3), len(j)) if len(j) > 2 else (None, len(j))


def main():
    out = []
    m = pd.read_csv("results/main.csv")
    for tag in ("haiku", "gpt"):
        judge_swap(m, tag, out)
    _rest(m, out)


def judge_swap(m, tag, out):
    alt = m[m.condition.str.endswith(f"~{tag}")].copy()
    if len(alt):
        alt["base"] = alt.condition.str.replace(f"~{tag}", "", regex=False)
        base = m.set_index("condition")
        a = alt.set_index("base")
        for metric in ("L3_loose", "iv_f1", "macro_f1", "false_per100"):
            r, n = rho(base[metric], a[metric])
            out.append({"check": f"judge Sonnet vs {tag}", "metric": metric, "spearman": r, "n_conditions": n})
        cmp = pd.DataFrame({"sonnet_L3": base.loc[a.index, "L3_loose"], f"{tag}_L3": a.L3_loose,
                            "sonnet_f1": base.loc[a.index, "iv_f1"], f"{tag}_f1": a.iv_f1,
                            "sonnet_false": base.loc[a.index, "false_per100"], f"{tag}_false": a.false_per100})
        print(f"Judge swap Sonnet -> {tag} (same memory, different judge):")
        print(cmp.round(3).to_string() + "\n")


def _rest(m, out):
    g1 = Path("results/retrieval_grid.csv"); g2 = Path("results/retrieval_grid_minilm.csv")
    if g1.exists() and g2.exists():
        def cells(path):
            d = pd.read_csv(path, keep_default_na=False)
            d = d[(d["mode"] == "proactive") & d.chunker.isin(list("ABCDE"))]
            return d.groupby(["chunker", "retriever"]).delivery.apply(lambda x: (x == "full").mean())
        c1, c2 = cells(g1), cells(g2)
        sel = [i for i in c1.index if i[1] != "bm25"]
        r, n = rho(c1.loc[sel], c2.loc[sel])
        out.append({"check": "embedding OpenAI vs MiniLM", "metric": "L2_full (emb+rrf cells)", "spearman": r, "n_conditions": n})
        r, n = rho(c1, c2)
        out.append({"check": "embedding OpenAI vs MiniLM", "metric": "L2_full (all 15 cells)", "spearman": r, "n_conditions": n})
        rows1 = c1.groupby(level=0).mean(); rows2 = c2.groupby(level=0).mean()
        print("\nEmbedding swap, chunker means (L2 full):")
        print(pd.DataFrame({"openai": rows1, "minilm": rows2}).round(3).to_string())
        print("col spread openai %.3f vs minilm %.3f" % (c1.groupby(level=1).mean().agg(lambda s: s.max() - s.min()),
                                                      c2.groupby(level=1).mean().agg(lambda s: s.max() - s.min())))
    # noise floor: same judge, same memory, a second batch run (tag ~s1)
    rep = m[m.condition.str.endswith("~s1")].copy()
    if len(rep):
        rep["base"] = rep.condition.str.replace("~s1", "", regex=False)
        base = m.set_index("condition")
        print("\nNoise floor (same judge + memory, run twice):")
        rows = []
        for r in rep.itertuples():
            b = base.loc[r.base]
            rows.append({"cond": r.base, "L3 run1": b.L3_loose, "L3 run2": r.L3_loose, "iv_f1 run1": b.iv_f1,
                         "iv_f1 run2": r.iv_f1, "false run1": b.false_per100, "false run2": r.false_per100})
            for metric in ("L3_loose", "iv_f1", "macro_f1", "false_per100"):
                out.append({"check": "noise: rerun", "metric": f"{metric} |run1-run2| {r.base}",
                            "spearman": round(abs(b[metric] - getattr(r, metric)), 3), "n_conditions": 1})
        print(pd.DataFrame(rows).round(3).to_string(index=False))
        try:
            import json as _j
            pts = {p["point_id"]: p for p in _j.load(open("data/eval_points.json"))}
            for r in rep.itertuples():
                a_ = {(_l := _j.loads(x))["point_id"]: _l["label"] for x in open(f"data/runs/{r.base}_b1500.jsonl")}
                b_ = {(_l := _j.loads(x))["point_id"]: _l["label"] for x in open(f"data/runs/{r.condition}_b1500.jsonl")}
                same = [a_[k] == b_[k] for k in a_ if k in b_]
                print(f"  {r.base}: identical label on {sum(same)}/{len(same)} points ({sum(same)/len(same):.0%})")
        except Exception as e:
            print("  (label agreement skipped:", e, ")")
    res = pd.DataFrame(out)
    res.to_csv("results/robustness.csv", index=False)
    print("\n" + res.to_string(index=False))


if __name__ == "__main__":
    main()
