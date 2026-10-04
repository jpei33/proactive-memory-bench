"""Export the labeling sheets (step 2.5).

    python -m label.export_sheet

Sheets (rows shuffled; nothing in them reveals which rows are plants):
  overlap        (100 rows) = 50 plant/decoy triggers (stratified by type) + 50 ordinary points.
                 Labeled by BOTH you and your friend -> human-human kappa, consensus labels,
                 and dev (30) / test (70) data for calibrating the LLM labeler.
  triggers_rest  (32 rows)  = the other plant/decoy triggers, labeled by you only, so every
                 planted label still gets a human check.
The remaining 100 ordinary points are labeled later by the calibrated LLM labeler.
plant_after points need no label (scoring uses their plant's label).

Files written
  label/sheet_overlap.md              rows to read (team facts + recent messages), with the rubric
  label/sheet_overlap_justin.csv      your answers:  row,label,severity,notes
  label/sheet_overlap_friend.csv      friend's answers (same blank form)
  label/sheet_overlap_gsheet.csv      everything in one table, for importing into Google Sheets
  label/sheet_triggers_rest.md / sheet_triggers_rest_justin.csv
  data/gold/sheet_key.json            row -> point mapping and planted labels (do NOT share)
"""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

from label.context import decision_line, load_ws, recent, team_facts, today

N_OVERLAP_TRIGGERS = 50
N_OVERLAP_ORDINARY = 50
INSTRUCTIONS = (
    "For each row, decide what an AI teammate with perfect memory should do right after the marked "
    "**decision message**: IGNORE, TRACK or INTERVENE, plus severity 1-3 (TRACK is always 1). "
    "Follow rubric.md (read it first). Notes are optional: for INTERVENE say which fact you act on, "
    "for TRACK what to check and by when, and flag anything you were unsure about.\n\n"
    "Suggested order for each row:\n"
    "1. Read the decision message. Note any date, number, name, owner, ticket, price or promise in it.\n"
    "2. Look each one up in the team facts (shown again below the messages). Different from the current "
    "value = contradiction; matches a \"previously\" value = stale; asks about something already in the "
    "facts = repeat question.\n"
    "3. Compare open items' check points with Today.\n"
    "4. Scan the recent messages: already corrected or answered? self-correction? proposal? addressed to "
    "a specific person? personal? -> IGNORE (tie-breaks 1-3, 11, 12).\n"
    "5. Nothing triggered -> IGNORE, unless the message opens a new commitment with an owner and a "
    "check point -> TRACK.")


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
        dec, day = decision_line(msgs, p["seq"]), today(msgs, p["seq"])
        md += [f"## Row {row}", "", f"**Today: {day}** · {p['channel']}", "",
               "**Team facts as of now**", "", facts, "",
               "**Recent messages** (oldest first; the last one is the decision message)", "",
               "```", rec, "```", "",
               f"> **>>> DECIDE AFTER THIS:** {dec}", "",
               "**Team facts again**", "", facts, "", "---", ""]
        rows.append((row, day, facts, rec, dec))
    return "\n".join(md), rows


def stratified_triggers(triggers, n, rng, type_of):
    """n triggers, allocated across plant/decoy types in proportion (at least 1 per type)."""
    by_t = {}
    for p in triggers:
        by_t.setdefault(type_of[p["plant_id"]], []).append(p)
    types = sorted(by_t)
    alloc = {t: max(1, round(n * len(by_t[t]) / len(triggers))) for t in types}
    while sum(alloc.values()) > n:                      # trim the largest groups first
        t = max(types, key=lambda t: (alloc[t], len(by_t[t])))
        alloc[t] -= 1
    while sum(alloc.values()) < n:                      # top up groups with spare items
        t = max((t for t in types if alloc[t] < len(by_t[t])), key=lambda t: len(by_t[t]) - alloc[t])
        alloc[t] += 1
    out = []
    for t in types:
        out += rng.sample(by_t[t], alloc[t])
    return out


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
    type_of = {}
    for ws in sorted({p["ws"] for p in points}):
        for pl in load_ws(ws)[2]:
            type_of[pl["plant_id"]] = pl["type"]
    ov_trig = stratified_triggers(triggers, N_OVERLAP_TRIGGERS, rng, type_of)
    ov_ord = per_ws_sample(ordinary, N_OVERLAP_ORDINARY, rng)
    overlap = ov_trig + ov_ord
    rest = [p for p in triggers if p not in ov_trig]
    rng.shuffle(overlap)
    rng.shuffle(rest)

    cache, key = {}, []
    for name, pts, title in (("overlap", overlap, f"Labeling sheet: overlap ({len(overlap)} rows)"),
                             ("triggers_rest", rest, f"Labeling sheet: triggers_rest ({len(rest)} rows)")):
        md, rows = render(pts, title, cache)
        Path(f"label/sheet_{name}.md").write_text(md)
        blank_form(f"label/sheet_{name}_justin.csv", len(pts))
        if name == "overlap":
            blank_form("label/sheet_overlap_friend.csv", len(pts))
            with open("label/sheet_overlap_gsheet.csv", "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["row", "today", "decision_message", "team_facts", "recent_messages",
                            "label", "severity", "notes"])
                for row, day, facts, rec, dec in rows:
                    w.writerow([row, day, dec, facts, rec, "", "", ""])
        for row, p in enumerate(pts, 1):
            key.append({"sheet": name, "row": row, "point_id": p["point_id"], "kind": p["kind"],
                        "plant_id": p.get("plant_id"), "gold_label": p.get("gold_label"),
                        "severity": p.get("severity")})
    Path("data/gold/sheet_key.json").write_text(json.dumps(key, indent=1))
    print(f"overlap:       {len(overlap)} rows ({len(ov_trig)} triggers + {len(ov_ord)} ordinary) -> label/sheet_overlap.md  [you + friend]")
    print(f"triggers_rest: {len(rest)} rows (triggers)                      -> label/sheet_triggers_rest.md  [you]")
    print(f"ordinary points left for the LLM labeler: {len(ordinary) - len(ov_ord)}")
    print("key -> data/gold/sheet_key.json (don't share)")


if __name__ == "__main__":
    main()
