"""Print the retrieval-grid pivots (draft figure 1).

    python -m eval.grid_table [--csv results/retrieval_grid.csv] [--mode proactive|reactive]

Pivot 1: chunker x retriever, % full delivery (plants + probe triggers), with row/column means.
Pivot 2: chunker (its best retriever) x origin evidence form, % full ORIGIN delivery.
Pivot 3: chunker (best retriever) x bucket and x structure, % full delivery.
"""
from __future__ import annotations

import argparse

import pandas as pd

ORDER = ["window", "A", "B", "C", "Cstar", "D", "E", "oracle"]
FORMS = ["explicit", "ellipsis", "reaction", "correction", "cross_ref", "distributed"]


def pct(s):
    return round(100 * (s == "full").mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="results/retrieval_grid.csv")
    ap.add_argument("--mode", default="proactive")
    a = ap.parse_args()
    df = pd.read_csv(a.csv, keep_default_na=False)
    df = df[df["mode"] == a.mode]
    n_q = df[df.chunker == "window"].groupby("query_kind").size().to_dict()
    print(f"mode={a.mode}  queries: {n_q}\n")

    grid = df[~df.chunker.isin(["window", "oracle"])]
    p1 = grid.pivot_table(index="chunker", columns="retriever", values="delivery", aggfunc=pct)
    p1 = p1.reindex([c for c in ORDER if c in p1.index])
    p1["row mean"] = p1.mean(axis=1).round()
    p1.loc["col mean"] = p1.mean().round()
    base = {c: pct(df[df.chunker == c]["delivery"]) for c in ("window", "oracle")}
    print("Pivot 1: % full delivery (chunker x retriever)")
    print(p1.astype(int).to_string())
    print(f"baselines: window-only {base['window']}%, oracle {base['oracle']}%")
    rows_spread = p1.drop("col mean")["row mean"].max() - p1.drop("col mean")["row mean"].min()
    cols_spread = p1.loc["col mean"].drop("row mean").max() - p1.loc["col mean"].drop("row mean").min()
    print(f"spread across chunkers {rows_spread:.0f} pts vs across retrievers {cols_spread:.0f} pts "
          f"-> {'chunking matters more' if rows_spread > cols_spread else 'retrieval matters as much or more'}\n")

    best = p1.drop("col mean").drop(columns="row mean").idxmax(axis=1).to_dict()
    sel = pd.concat([grid[(grid.chunker == c) & (grid.retriever == r)] for c, r in best.items()]
                    + [df[df.chunker.isin(["window", "oracle"])]])
    sel = sel.assign(cond=sel.chunker + sel.chunker.map(lambda c: f" ({best[c]})" if c in best else ""))
    order = [c + (f" ({best[c]})" if c in best else "") for c in ORDER if c in best or c in ("window", "oracle")]

    p2 = sel.pivot_table(index="cond", columns="evidence_form", values="origin_delivery", aggfunc=pct)
    p2 = p2.reindex(order)[[f for f in FORMS if f in p2.columns]]
    n2 = sel[sel.chunker == "window"].groupby("evidence_form").size()
    print("Pivot 2: % full ORIGIN delivery (chunker @ best retriever x evidence form)")
    print(p2.to_string())
    print("n per form:", n2.reindex(p2.columns).to_dict(), "\n")

    for col in ("bucket", "structure"):
        p = sel.pivot_table(index="cond", columns=col, values="delivery", aggfunc=pct).reindex(order)
        print(f"Pivot 3 ({col}): % full delivery")
        print(p.to_string())
        print("n:", sel[sel.chunker == "window"].groupby(col).size().to_dict(), "\n")


if __name__ == "__main__":
    main()
