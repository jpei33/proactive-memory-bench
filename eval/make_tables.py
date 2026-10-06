"""Summary tables for the README (no API calls; reads results/*.csv).

    python -m eval.make_tables
      -> results/strategy_table.md        15 memory strategies (5 chunkers x 3 retrievers) + reference rows
      -> results/probe_table.md           paired-probe decisions for the conditions that ran on them
      -> results/figs/strategy_table.png  the strategy table as an image
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

CHUNK = {"A": "A · per message", "B": "B · 6-msg window", "C": "C · reply-linked (inferred)",
         "D": "D · topic segments", "E": "E · write-time rewrite"}
RET = {"1": "BM25", "2": "embeddings", "3": "hybrid (RRF)"}
RNAME = {"1": "bm25", "2": "emb", "3": "rrf"}


def pct(x):
    return "" if pd.isna(x) else f"{100 * x:.0f}"


def build():
    grid = pd.read_csv("results/retrieval_grid.csv", keep_default_na=False)
    main = pd.read_csv("results/main.csv").set_index("condition")

    def deliv(chunker, retr, mode):
        g = grid[(grid["mode"] == mode) & (grid.chunker == chunker) & (grid.retriever == retr)]
        if mode == "reactive":
            g = g[g.query_kind == "plant"]
        return (g.delivery == "full").mean() if len(g) else float("nan")

    rows = []
    for c in "ABCDE":
        for r in "123":
            cond = f"{c}{r}"
            m = main.loc[cond]
            rows.append({"Strategy": cond, "Chunking": CHUNK[c], "Retriever": RET[r],
                         "Proactive delivery %": deliv(c, RNAME[r], "proactive"),
                         "Reactive delivery %": deliv(c, RNAME[r], "reactive"),
                         "Plants caught %": m.L3_loose, "INTERVENE F1": m.iv_f1,
                         "False alarms /100": m.false_per100, "$ / 1k decisions": m.usd_per_1k})
    refs = [("S0", "window only (no memory)", "-", ("window", "-")),
            ("Cs2", "Cstar · reply-linked (gold links)", "embeddings", ("Cstar", "emb")),
            ("AG-grep", "agent searches: grep + read-around", "tools", None),
            ("AG-both", "agent searches: + semantic search", "tools", None),
            ("OR", "oracle facts box (perfect memory)", "-", ("oracle", "-"))]
    for cond, chunking, retr, key in refs:
        m = main.loc[cond]
        rows.append({"Strategy": cond, "Chunking": chunking, "Retriever": retr,
                     "Proactive delivery %": deliv(*key, "proactive") if key else float("nan"),
                     "Reactive delivery %": deliv(*key, "reactive") if key else float("nan"),
                     "Plants caught %": m.L3_loose, "INTERVENE F1": m.iv_f1,
                     "False alarms /100": m.false_per100, "$ / 1k decisions": m.usd_per_1k})
    return pd.DataFrame(rows)


def to_md(df, n_grid=15):
    best = {"Proactive delivery %": df.iloc[:n_grid]["Proactive delivery %"].max(),
            "Plants caught %": df.iloc[:n_grid]["Plants caught %"].max(),
            "INTERVENE F1": df.iloc[:n_grid]["INTERVENE F1"].max()}
    out = []
    for i, r in df.iterrows():
        def f(col, fmt):
            v = r[col]
            s = "" if pd.isna(v) else fmt(v)
            return f"**{s}**" if i < n_grid and col in best and v == best[col] else s
        out.append({"Strategy": r.Strategy, "Chunking": r.Chunking, "Retriever": r.Retriever,
                    "Retrieval: proactive %": f("Proactive delivery %", pct),
                    "Retrieval: reactive %": f("Reactive delivery %", pct),
                    "Judge: plants caught %": f("Plants caught %", pct),
                    "Judge: INTERVENE F1": f("INTERVENE F1", lambda v: f"{v:.2f}"),
                    "Judge: false alarms /100": f("False alarms /100", lambda v: f"{v:.1f}"),
                    "$ / 1k decisions": f("$ / 1k decisions", lambda v: f"{v:.2f}")})
    t = pd.DataFrame(out)
    md = t.iloc[:n_grid].to_markdown(index=False)
    ref = t.iloc[n_grid:].to_markdown(index=False).splitlines()[2:]
    sep = "| " + " | ".join(["*reference*"] + [""] * (t.shape[1] - 1)) + " |"
    return md + "\n" + sep + "\n" + "\n".join(ref)


def probe_md():
    p = pd.read_csv("results/probe_decisions.csv")
    name = {"S0": "window only", "A3": "A · per message + RRF", "B3": "B · window + RRF", "Cs2": "Cstar · gold links + emb",
            "D2": "D · topics + emb", "E1": "E · rewrite + BM25", "AG-grep": "agent searches (grep)", "OR": "oracle facts box"}
    rows = [{"Condition": f"{r.condition} ({name.get(r.condition, '')})",
             "Evidence delivered %": pct(r.delivered_full),
             "Catches wrong value % [95% CI]": f"{100*r.catch:.0f} [{100*r.catch_lo:.0f}, {100*r.catch_hi:.0f}]",
             "False alarm on correct value %": f"{100*r.false_alarm:.0f}",
             "Balanced acc. %": f"{100*r.bal_acc:.0f}",
             "Catch given evidence delivered %": pct(r["catch|full"])} for _, r in p.iterrows()]
    return pd.DataFrame(rows).to_markdown(index=False)


def png(df, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cols = ["Strategy", "Chunking", "Retriever", "Proactive delivery %", "Reactive delivery %",
            "Plants caught %", "INTERVENE F1", "False alarms /100", "$ / 1k decisions"]
    head = ["", "Chunking", "Retriever", "Retrieval\nproactive %", "Retrieval\nreactive %",
            "Judge: plants\ncaught %", "Judge\nINTERVENE F1", "Judge: false\nalarms /100", "$ per 1k\ndecisions"]
    cells = []
    for _, r in df[cols].iterrows():
        cells.append([r.Strategy, r.Chunking, r.Retriever, pct(r["Proactive delivery %"]), pct(r["Reactive delivery %"]),
                      pct(r["Plants caught %"]), "" if pd.isna(r["INTERVENE F1"]) else f"{r['INTERVENE F1']:.2f}",
                      f"{r['False alarms /100']:.1f}", f"{r['$ / 1k decisions']:.2f}"])
    fig, ax = plt.subplots(figsize=(13.5, 0.32 * (len(cells) + 2)))
    ax.axis("off")
    tb = ax.table(cellText=cells, colLabels=head, cellLoc="center", bbox=[0, 0, 1, 1],
                  colWidths=[.06, .23, .09, .09, .09, .1, .09, .1, .08])
    tb.auto_set_font_size(False)
    tb.set_fontsize(9)
    n = 15
    for (i, j), c in tb.get_celld().items():
        c.set_edgecolor("#d0d0d0")
        if i == 0:
            c.set_facecolor("#1f3b4d"); c.get_text().set_color("white"); c.get_text().set_weight("bold")
        elif i > n:
            c.set_facecolor("#f2f2f2")
        elif (i - 1) // 3 % 2 == 1:
            c.set_facecolor("#f8fbfd")
        if j == 1 and i > 0:
            c.get_text().set_ha("left")
    for col, j in (("Proactive delivery %", 3), ("Plants caught %", 5), ("INTERVENE F1", 6)):
        best = df.iloc[:n][col].idxmax()
        tb[(best + 1, j)].get_text().set_weight("bold")
    ax.set_title("15 memory strategies (5 chunkers × 3 retrievers) + reference conditions\n"
                 "Retrieval: % of queries where all evidence reached the agent (1,500-token budget). "
                 "Judge (Sonnet): 36 planted conflicts, 232 decision points.", fontsize=10, loc="left", pad=10)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")


def main():
    df = build()
    Path("results/figs").mkdir(parents=True, exist_ok=True)
    Path("results/strategy_table.md").write_text(to_md(df) + "\n")
    Path("results/probe_table.md").write_text(probe_md() + "\n")
    png(df, "results/figs/strategy_table.png")
    print(to_md(df)); print(); print(probe_md())
    print("\n-> results/strategy_table.md, results/probe_table.md, results/figs/strategy_table.png")


if __name__ == "__main__":
    main()
