"""Render the eval points not in any human sheet as label/sheet_ordinary_rest.md, for the LLM labeler.

    python -m label.export_rest

Leaves sheet_overlap / sheet_triggers_rest untouched; appends sheet='ordinary_rest' rows to
data/gold/sheet_key.json (replacing any earlier ordinary_rest rows).
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from label.export_sheet import render

KEY = Path("data/gold/sheet_key.json")


def main(seed: int = 13):
    points = json.load(open("data/eval_points.json"))
    key = [k for k in json.load(open(KEY)) if k["sheet"] != "ordinary_rest"]
    used = {k["point_id"] for k in key}
    rest = [p for p in points if p["point_id"] not in used]
    random.Random(seed).shuffle(rest)
    md, _ = render(rest, f"Labeling sheet: ordinary_rest ({len(rest)} rows, LLM-labeled)", {})
    Path("label/sheet_ordinary_rest.md").write_text(md)
    for row, p in enumerate(rest, 1):
        key.append({"sheet": "ordinary_rest", "row": row, "point_id": p["point_id"], "kind": p["kind"],
                    "plant_id": p.get("plant_id"), "gold_label": p.get("gold_label"),
                    "severity": p.get("severity")})
    KEY.write_text(json.dumps(key, indent=1))
    kinds = {}
    for p in rest:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    print(f"{len(rest)} points {kinds} -> label/sheet_ordinary_rest.md; key updated")


if __name__ == "__main__":
    main()
