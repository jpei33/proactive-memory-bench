"""Export the labeling sheets (step 2.5).

    python -m label.export_sheet

Sheets (rows shuffled; nothing in them reveals which rows are plants):
  overlap  (150 rows) = all 82 plant + decoy triggers + 68 ordinary points.
           Labeled by BOTH you and your friend -> human-human kappa, consensus labels,
           and dev/test data for calibrating the LLM labeler.
  extra    (50 rows)  = 50 more ordinary points, labeled by you only.
The remaining ordinary points are labeled later by the calibrated LLM labeler.
plant_after points need no label (scoring uses their plant's label).

Files written
  label/sheet_overlap.md              rows to read (team facts + recent messages), with the rubric
  label/sheet_overlap_justin.csv      your answers:  row,label,severity,notes
  label/sheet_overlap_friend.csv      friend's answers (same blank form)
  label/sheet_overlap_gsheet.csv      everything in one table, for importing into Google Sheets
  label/sheet_extra.md / sheet_extra_justin.csv
  data/gold/sheet_key.json            row -> point mapping and planted labels (do NOT share)
"""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

from label.context import load_ws, recent, team_facts

N_OVERLAP_ORDINARY = 68
N_EXTRA = 50
INSTRUCTIONS = (
    "For each row, read the team facts and the recent messages, then decide what an AI teammate "
    "with perfect memory should do right after the **last** message: IGNORE, TRACK or INTERVENE, "
    "plus severity 1-3 (TRACK is always 1). Follow rubric.md (read it first). Notes are optional: "
    "for INTERVENE say which fact you act on, for TRACK what to check and by when, and flag anything "
    "you were unsure about.")


def per_ws_sample(pool, n, rng):
    """Sample n points spread evenly across workspaces."""
    by_ws = {}
    for p in pool:
        by_ws.setdefault(p["ws"], []).append(p)
    names = sorted(by_ws)
    quota = {ws: n // len(names) + (i < n % len(names)) for i, ws in enumerate(names)}
    out = []
    for ws in names:
        out += rng.sample(by_ws[ws], min(quota[ws], len(by_ws[ws])))
    return out


def render(points, title, cache):
    md = [f"# {title}", "", INSTRUCTIONS, ""]
    rows = []
    for row, p in enumerate(points, 1):
        if p["ws"] not in cache:
            cache[p["ws"]] = load_ws(p["ws"])
        d, msgs, _ = cache[p["ws"]]
        facts, rec = team_facts(d, msgs, p["seq"]), recent(msgs, p["seq"], p["channel"])
        md += [f"## Row {row}", "", "**Team facts as of now**", "", facts, "",
               "**Recent messages** (the last one is the decision point)", "", "```", rec, "```", ""]
        rows.append((row, facts, rec))
    return "\n".join(md), rows


def blank_form(path, n):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row", "label", "severity", "notes"])
        for r in range(1, n + 1):
            w.writerow([r, "", "", ""])


def main(seed: int = 7):
    rng = random.Random(seed)
    points = json.load(open("data/eval_points.json"))
    triggers = [p for p in points if p["kind"] in ("plant_trigger", "decoy_trigger")]
    ordinary = [p for p in points if p["kind"] == "ordinary"]
    ov_ord = per_ws_sample(ordinary, N_OVERLAP_ORDINARY, rng)
    rest = [p for p in ordinary if p not in ov_ord]
    extra = per_ws_sample(rest, N_EXTRA, rng)
    overlap = triggers + ov_ord
    rng.shuffle(overlap)
    rng.shuffle(extra)

    cache, key = {}, []
    for name, pts, title in (("overlap", overlap, "Labeling sheet: overlap (150 rows)"),
                             ("extra", extra, "Labeling sheet: extra (50 rows)")):
        md, rows = render(pts, title, cache)
        Path(f"label/sheet_{name}.md").write_text(md)
        blank_form(f"label/sheet_{name}_justin.csv", len(pts))
        if name == "overlap":
            blank_form("label/sheet_overlap_friend.csv", len(pts))
            with open("label/sheet_overlap_gsheet.csv", "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["row", "team_facts", "recent_messages", "label", "severity", "notes"])
                for row, facts, rec in rows:
                    w.writerow([row, facts, rec, "", "", ""])
        for row, p in enumerate(pts, 1):
            key.append({"sheet": name, "row": row, "point_id": p["point_id"], "kind": p["kind"],
                        "plant_id": p.get("plant_id"), "gold_label": p.get("gold_label"),
                        "severity": p.get("severity")})
    Path("data/gold/sheet_key.json").write_text(json.dumps(key, indent=1))
    n_ov = sum(1 for k in key if k["sheet"] == "overlap")
    print(f"overlap: {n_ov} rows ({len(triggers)} triggers + {len(ov_ord)} ordinary)  -> label/sheet_overlap.md")
    print(f"extra:   {len(extra)} rows (ordinary)                -> label/sheet_extra.md")
    print(f"unlabeled ordinary points left for the LLM labeler: {len(ordinary) - len(ov_ord) - len(extra)}")
    print("key -> data/gold/sheet_key.json (don't share)")


if __name__ == "__main__":
    main()
