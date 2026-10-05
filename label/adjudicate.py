"""Blind adjudication of human-vs-model disagreements.

    python -m label.adjudicate label/sheet_overlap_justin.csv label/sheet_overlap_gpt-6-luna_v2.csv
        -> label/sheet_adjudicate.md   (each disagreement row, two candidate labels in random order,
                                        not saying which is yours or the model's)
        -> label/sheet_adjudicate.csv  (row,label,severity,notes: fill label with your final call)
    python -m label.adjudicate label/sheet_overlap_justin.csv label/sheet_overlap_gpt-6-luna_v2.csv --merge
        -> label/sheet_overlap_adjudicated.csv  (your first pass, with the adjudicated rows replaced)

Your first-pass file is never modified. Planted labels are not shown.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
from pathlib import Path

from label.llm_label import rows_from_sheet


def sheet_of(path):
    """'label/sheet_triggers_rest_justin.csv' -> 'triggers_rest' (longest known sheet name that fits)."""
    name = Path(path).name
    known = {k["sheet"] for k in json.load(open("data/gold/sheet_key.json"))}
    fits = [s for s in known if name.startswith(f"sheet_{s}_")]
    if not fits:
        raise SystemExit(f"can't tell which sheet {name} belongs to (known: {sorted(known)})")
    return max(fits, key=len)


def load(path):
    return {int(r["row"]): r for r in csv.DictReader(open(path)) if r["label"].strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("human")
    ap.add_argument("model")
    ap.add_argument("--merge", action="store_true")
    x = ap.parse_args()
    sheet = sheet_of(x.human)
    H, M = load(x.human), load(x.model)
    dis = sorted(r for r in set(H) & set(M) if H[r]["label"].strip().upper() != M[r]["label"].strip().upper())
    tag = "" if sheet == "overlap" else f"_{sheet}"   # overlap keeps the original file names
    md, sheet_csv = Path(f"label/sheet_adjudicate{tag}.md"), Path(f"label/sheet_adjudicate{tag}.csv")
    out = Path(f"label/sheet_{sheet}_adjudicated.csv")

    if x.merge:
        adj = {int(r["row"]): r for r in csv.DictReader(open(sheet_csv)) if r["label"].strip()}
        missing = [r for r in dis if r not in adj]
        if missing:
            raise SystemExit(f"still blank in {sheet_csv}: rows {missing}")
        final = {r: dict(H[r]) for r in H}
        changed = 0
        for r, a in adj.items():
            new = {"row": r, "label": a["label"].strip().upper(), "severity": a.get("severity", ""),
                   "notes": a.get("notes", "")}
            changed += new["label"] != H[r]["label"].strip().upper()
            final[r] = new
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["row", "label", "severity", "notes"], extrasaction="ignore")
            w.writeheader()
            for r in sorted(final):
                w.writerow(final[r])
        print(f"-> {out}: {len(adj)} rows adjudicated, {changed} changed from your first pass")
        return

    text = rows_from_sheet(sheet)
    rng = random.Random(31)
    parts = ["# Adjudication sheet\n",
             "Each row below got two different labels. One is your first pass, one is the model's, in random",
             f"order. Reread the row against rubric.md and write your FINAL label in {sheet_csv.name}.",
             "You may pick either candidate or a third label.\n"]
    for r in dis:
        c = [H[r]["label"].strip().upper(), M[r]["label"].strip().upper()]
        rng.shuffle(c)
        parts += [f"\n## Row {r}\n", f"**Candidates:** {c[0]} / {c[1]}\n", text[r], "\n---"]
    md.write_text("\n".join(parts) + "\n")
    with open(sheet_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row", "label", "severity", "notes"])
        for r in dis:
            w.writerow([r, "", "", ""])
    print(f"{len(dis)} disagreements -> {md}, fill {sheet_csv}, then rerun with --merge")


if __name__ == "__main__":
    main()
