"""Blind re-label of 30 overlap rows, for your self-agreement (intra-rater) score.
Run this a day or more after your first pass, so you don't remember your answers.

    python -m label.relabel            # writes label/sheet_relabel.md + label/sheet_relabel_justin.csv
    python -m label.relabel --score    # after labeling: kappa between your two passes
"""
import argparse
import csv
import json
import random
from pathlib import Path

from label.llm_label import rows_from_sheet

N, SEED = 30, 23


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--score", action="store_true")
    a = ap.parse_args()
    if a.score:
        from sklearn.metrics import cohen_kappa_score
        m = json.load(open("data/gold/relabel_map.json"))
        first = {int(r["row"]): r["label"].strip().upper() for r in csv.DictReader(open("label/sheet_overlap_justin.csv"))}
        second = {int(r["row"]): r["label"].strip().upper() for r in csv.DictReader(open("label/sheet_relabel_justin.csv")) if r["label"].strip()}
        pairs = [(first[m[str(r)]], second[r]) for r in second]
        print(f"{len(pairs)} rows: raw agreement {sum(x == y for x, y in pairs) / len(pairs):.2f}, "
              f"kappa {cohen_kappa_score(*zip(*pairs), labels=['IGNORE', 'TRACK', 'INTERVENE']):.3f}")
        for r in second:
            if first[m[str(r)]] != second[r]:
                print(f"  relabel row {r} (overlap row {m[str(r)]}): first {first[m[str(r)]]}, now {second[r]}")
        return
    rows = rows_from_sheet("overlap")
    seen = set()                                     # rows you re-read during adjudication: skip them
    if Path("label/sheet_adjudicate.csv").exists():
        seen = {int(r["row"]) for r in csv.DictReader(open("label/sheet_adjudicate.csv"))}
    pick = random.Random(SEED).sample(sorted(set(rows) - seen), N)
    md = ["# Re-label sheet (30 rows)", "", "Same task and rubric as before. Label each row fresh; don't look up "
          "your earlier answers.", ""]
    mapping = {}
    for i, r in enumerate(pick, 1):
        md += [f"## Row {i}", "", rows[r], "", "---", ""]
        mapping[i] = r
    Path("label/sheet_relabel.md").write_text("\n".join(md))
    with open("label/sheet_relabel_justin.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row", "label", "severity", "notes"])
        for i in range(1, N + 1):
            w.writerow([i, "", "", ""])
    Path("data/gold/relabel_map.json").write_text(json.dumps(mapping, indent=1))
    print("wrote label/sheet_relabel.md + label/sheet_relabel_justin.csv (30 rows); map -> data/gold/relabel_map.json")


if __name__ == "__main__":
    main()
