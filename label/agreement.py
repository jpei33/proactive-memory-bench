"""Agreement between two label files on the same sheet, plus each vs the planted labels.

    python -m label.agreement label/sheet_overlap_justin.csv label/sheet_overlap_<model>_v1.csv
    python -m label.agreement A.csv B.csv --split dev       # overlap dev rows only (30)
    python -m label.agreement A.csv B.csv --split test      # held-out rows (70)
    python -m label.agreement A.csv --split dev             # B = newest model CSV for that sheet

Prints Cohen's kappa (3-class, linear-weighted, binary INTERVENE), raw agreement, a confusion
matrix, agreement with planted labels on trigger rows, and every disagreement with its decision
message so you can adjudicate.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from sklearn.metrics import cohen_kappa_score, confusion_matrix

from label.llm_label import rows_from_sheet, split_rows

LABELS = ["IGNORE", "TRACK", "INTERVENE"]
ORD = {l: i for i, l in enumerate(LABELS)}


def sheet_of(path):
    """'label/sheet_triggers_rest_justin.csv' -> 'triggers_rest' (longest known sheet name that fits)."""
    name = Path(path).name
    known = {k["sheet"] for k in json.load(open("data/gold/sheet_key.json"))}
    fits = [s for s in known if name.startswith(f"sheet_{s}_")]
    if not fits:
        raise SystemExit(f"can't tell which sheet {name} belongs to (known: {sorted(known)})")
    return max(fits, key=len)


def load(path):
    return {int(r["row"]): r["label"].strip().upper() for r in csv.DictReader(open(path)) if r["label"].strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b", nargs="?", help="default: newest model CSV for the same sheet")
    ap.add_argument("--split", default="all", choices=["all", "dev", "test"])
    x = ap.parse_args()
    sheet = sheet_of(x.a)
    if x.b is None:
        human = ("justin", "friend", "gsheet")
        cands = [p for p in Path(x.a).parent.glob(f"sheet_{sheet}_*.csv")
                 if not any(p.stem.endswith("_" + h) for h in human)]
        if not cands:
            raise SystemExit(f"no model CSV found for sheet '{sheet}'; run label.llm_label first")
        x.b = str(max(cands, key=lambda p: p.stat().st_mtime))
        print(f"(comparing against {x.b})")
    A, B = load(x.a), load(x.b)
    rows = sorted(set(A) & set(B))
    if sheet == "overlap":
        rows = [r for r in rows if r in split_rows()[x.split]]
    a, b = [A[r] for r in rows], [B[r] for r in rows]
    print(f"{sheet} sheet, split={x.split}: {len(rows)} rows labeled by both")
    print(f"  raw agreement        {sum(i == j for i, j in zip(a, b)) / len(rows):.2f}")
    print(f"  kappa (3-class)      {cohen_kappa_score(a, b, labels=LABELS):.3f}")
    print(f"  kappa (weighted)     {cohen_kappa_score([ORD[i] for i in a], [ORD[j] for j in b], weights='linear'):.3f}")
    print(f"  kappa (INTERVENE?)   {cohen_kappa_score([i == 'INTERVENE' for i in a], [j == 'INTERVENE' for j in b]):.3f}")
    cm = confusion_matrix(a, b, labels=LABELS)
    print(f"\n  rows = {Path(x.a).stem}, cols = {Path(x.b).stem}")
    print("  " + " " * 10 + "".join(f"{l:>10}" for l in LABELS))
    for l, line in zip(LABELS, cm):
        print("  " + f"{l:<10}" + "".join(f"{v:>10}" for v in line))

    key = {k["row"]: k for k in json.load(open("data/gold/sheet_key.json")) if k["sheet"] == sheet}
    trig = [r for r in rows if key[r]["gold_label"]]
    if trig:
        for name, L in ((Path(x.a).stem, A), (Path(x.b).stem, B)):
            ok = sum(L[r] == key[r]["gold_label"] for r in trig)
            print(f"\n  {name} vs planted labels on trigger rows: {ok}/{len(trig)}")

    text = rows_from_sheet(sheet)
    dis = [r for r in rows if A[r] != B[r]]
    print(f"\n{len(dis)} disagreements:")
    for r in dis:
        dec = re.search(r">>> DECIDE AFTER THIS:\*\* (.+)", text[r])
        planted = key[r]["gold_label"] or "-"
        print(f"  row {r:>3}: A={A[r]:<9} B={B[r]:<9} planted={planted:<9} | {dec.group(1)[:90] if dec else ''}")


if __name__ == "__main__":
    main()
