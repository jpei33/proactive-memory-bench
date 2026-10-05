"""Assemble the final label for every eval point -> data/gold/labels.json.

    python -m label.build_gold [--model gpt-6-luna_v2]

Source per sheet (best available first):
  overlap        sheet_overlap_adjudicated.csv   (you, after blind adjudication vs the model)
  triggers_rest  sheet_triggers_rest_justin.csv  (you)
  ordinary_rest  sheet_ordinary_rest_<model>.csv (LLM labeler, validated on overlap)
Each entry records its source so results can be split by human- vs model-labeled points.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-6-luna_v2")
    x = ap.parse_args()
    src = {"overlap": ("label/sheet_overlap_adjudicated.csv", "human_adjudicated"),
           "triggers_rest": (("label/sheet_triggers_rest_adjudicated.csv", "human_adjudicated")
                             if Path("label/sheet_triggers_rest_adjudicated.csv").exists()
                             else ("label/sheet_triggers_rest_justin.csv", "human")),
           "ordinary_rest": (f"label/sheet_ordinary_rest_{x.model}.csv", f"llm:{x.model}")}
    labels = {}
    for sheet, (path, tag) in src.items():
        if Path(path).exists():
            labels[sheet] = ({int(r["row"]): r for r in csv.DictReader(open(path)) if r["label"].strip()}, tag)
        else:
            print(f"missing {path}")
    out, missing = [], []
    for k in json.load(open("data/gold/sheet_key.json")):
        rows, tag = labels.get(k["sheet"], ({}, None))
        r = rows.get(k["row"])
        if not r:
            missing.append(f"{k['sheet']}#{k['row']}")
            continue
        sev = r.get("severity", "").strip()
        out.append({"point_id": k["point_id"], "label": r["label"].strip().upper(),
                    "severity": int(sev) if sev.isdigit() else None, "source": tag,
                    "kind": k["kind"], "plant_id": k["plant_id"], "planted_label": k["gold_label"]})
    Path("data/gold/labels.json").write_text(json.dumps(out, indent=1))
    print(f"-> data/gold/labels.json: {len(out)} points")
    print("  by source:", dict(Counter(o["source"] for o in out)))
    print("  by label: ", dict(Counter(o["label"] for o in out)))
    if missing:
        print(f"  {len(missing)} without a label: {missing[:10]}{' ...' if len(missing) > 10 else ''}")


if __name__ == "__main__":
    main()
