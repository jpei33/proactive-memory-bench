"""Rubric pilot: 20 stratified decision points for you to label before freezing the rubric.

    python -m label.pilot           # writes label/pilot_20.md + label/pilot_20_labels.csv
    python -m label.check_pilot     # after labeling: agreement with the planted labels

Mix: 8 plant triggers (varied types), 5 decoy triggers, 2 follow-ups, 5 ordinary.
The answer key goes to data/gold/pilot_20_key.json; don't open it before labeling.
"""
from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from pathlib import Path

from label.context import load_ws, recent, team_facts

MIX = {"plant_trigger": 8, "decoy_trigger": 5, "plant_after": 2, "ordinary": 5}


def main(seed: int = 1):
    rng = random.Random(seed)
    points = json.load(open("data/eval_points.json"))
    plants = {}
    for ws in sorted({p["ws"] for p in points}):
        for p in load_ws(ws)[2]:
            plants[p["plant_id"]] = p

    pick = []
    for kind, n in MIX.items():
        pool = [p for p in points if p["kind"] == kind]
        if kind in ("plant_trigger", "decoy_trigger"):          # round-robin over types for variety
            by_type = defaultdict(list)
            for p in pool:
                by_type[plants[p["plant_id"]]["type"]].append(p)
            types = sorted(by_type)
            rng.shuffle(types)
            for t in types:
                rng.shuffle(by_type[t])
            got, i = [], 0
            while len(got) < n:
                t = types[i % len(types)]
                if by_type[t]:
                    got.append(by_type[t].pop())
                i += 1
            pick += got
        else:
            pick += rng.sample(pool, n)
    rng.shuffle(pick)

    cache, md, key = {}, ["# Rubric pilot: 20 decision points", "",
                          "For each row, read the team facts and the recent messages, then decide what an AI "
                          "teammate with perfect memory should do right after the **last** message: IGNORE, TRACK "
                          "or INTERVENE, plus severity 1-3 (TRACK is always 1). Use rubric.md. Fill in "
                          "label/pilot_20_labels.csv.", ""], []
    for row, p in enumerate(pick, 1):
        if p["ws"] not in cache:
            cache[p["ws"]] = load_ws(p["ws"])
        d, msgs, _ = cache[p["ws"]]
        md += [f"## Row {row}", "", "**Team facts as of now**", "", team_facts(d, msgs, p["seq"]), "",
               "**Recent messages** (the last one is the decision point)", "", "```",
               recent(msgs, p["seq"], p["channel"]), "```", ""]
        pl = plants.get(p.get("plant_id") or "")
        key.append({"row": row, "point_id": p["point_id"], "kind": p["kind"], "plant_id": p.get("plant_id"),
                    "type": pl["type"] if pl and p["kind"].endswith("trigger") else None,
                    "gold_label": p.get("gold_label"), "severity": p.get("severity")})
    Path("label/pilot_20.md").write_text("\n".join(md))
    with open("label/pilot_20_labels.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row", "label", "severity", "notes"])
        for row in range(1, len(pick) + 1):
            w.writerow([row, "", "", ""])
    Path("data/gold/pilot_20_key.json").write_text(json.dumps(key, indent=1))
    print(f"wrote label/pilot_20.md and label/pilot_20_labels.csv ({len(pick)} rows); key -> data/gold/pilot_20_key.json")


if __name__ == "__main__":
    main()
