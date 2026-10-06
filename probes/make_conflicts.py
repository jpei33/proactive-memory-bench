"""Paired conflict / control probes: decision-level n without labeling (verification item 1).

    python -m probes.make_conflicts            # -> probes/conflicts.jsonl + data/probe_points.json
    python -m probes.make_conflicts --dry      # wrong-value plan only, no API calls

For each probe trigger position (probes/triggers.jsonl, 155 rows) Haiku writes ONE casual message in two
versions that differ only in the value:
  conflict : states the fact with a WRONG value, as if it were true      -> gold INTERVENE
  control  : the same message with the CURRENT value                      -> gold IGNORE
Wrong value = the fact's most recent earlier value if one exists at that point (a stale quote), else a
plausible invented alternative written by Haiku (a contradiction). Messages are checked with the same
value regexes as the simulator: conflict must contain the wrong value and not the current one; control
the reverse. Like probe triggers, these are virtual: never inserted into the chat; the judge sees them
as the newest message just before q_seq.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from memory.base import load_msgs
from sim.run_workspace import load, value_regex, vpat

PAIR = """Write one short, casual chat message from {PERSONA} ({ROLE}) in {CHANNEL} that states the
{ENTITY} ({ATTRIBUTE}) as a plain fact while getting on with their work (planning around it,
updating someone, drafting something). Write it in TWO versions that are identical except for the value:
version A uses "{WRONG}", version B uses "{CURRENT}". Do not hedge, ask, or propose; state it as settled.
Under 30 words. Return JSON only: {"A": "...", "B": "..."}"""

INVENT = """A team chat tracks this fact: {ENTITY} ({ATTRIBUTE}) = "{CURRENT}".
Give one plausible but different value of the same type and format (a different date, number, name,
policy...). Return only the value."""

OUT = Path("probes/conflicts.jsonl")
POINTS = Path("data/probe_points.json")


def stale_value(d, msgs_by_id, ws, fact, current, q_seq):
    """Most recent value of the fact set before q_seq that differs from the current value."""
    sets = []
    for h in d["_fact"][fact]["history"]:
        m = msgs_by_id.get(f"{ws}/{h['set_in']}/{h['turn']:03d}")
        if m and m["seq"] < q_seq:
            sets.append((m["seq"], h["value"]))
    olds = [v for _, v in sorted(sets) if v != current]
    return olds[-1] if olds else None


def make_one(job):
    from sim.llm import complete, parse_json
    model = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")
    d, row, wrong, kind = job
    rng = random.Random(row["probe_id"])
    cur = row["value"]
    if wrong is None:                                   # invent a plausible alternative
        for k in range(4):
            w = complete(None, INVENT.replace("{ENTITY}", row["entity"]).replace("{ATTRIBUTE}", row["attribute"])
                         .replace("{CURRENT}", cur), model=model, max_tokens=40, seed=k).text.strip().strip('"').strip()
            if w and not vpat(d, row["fact_id"], cur).search(w) and len(w) < 120:
                wrong = w
                break
        if wrong is None:
            return None
    p_cur = vpat(d, row["fact_id"], cur)
    try:
        p_wrong = vpat(d, row["fact_id"], wrong) if kind == "stale" else value_regex(wrong)
    except re.error:
        p_wrong = re.compile(re.escape(wrong), re.I)
    for k in range(6):
        sp = rng.choice(row["speakers"]) if row.get("speakers") else row["speaker"]
        per = d["_persona"][sp]
        prompt = (PAIR.replace("{PERSONA}", per["name"]).replace("{ROLE}", per["role"])
                  .replace("{CHANNEL}", row["channel"]).replace("{ENTITY}", row["entity"])
                  .replace("{ATTRIBUTE}", row["attribute"]).replace("{WRONG}", wrong).replace("{CURRENT}", cur))
        try:
            j = parse_json(complete(None, prompt, model=model, max_tokens=300, seed=k).text)
            a, b = str(j["A"]).strip(), str(j["B"]).strip()
        except (ValueError, KeyError, TypeError):
            continue
        if any(ch in a + b for ch in "{}") or a.startswith('"') or b.startswith('"'):
            continue                                    # JSON debris inside a version: resample
        if p_wrong.search(a) and not p_cur.search(a) and p_cur.search(b) and not p_wrong.search(b):
            return {**{k_: row[k_] for k_ in ("probe_id", "ws", "q_seq", "anchor_msg", "channel", "thread",
                                               "fact_id", "entity", "attribute", "evidence_groups", "origin_form",
                                               "bucket", "distance_msgs")},
                    "current": cur, "wrong": wrong, "conflict_kind": kind, "speaker": sp,
                    "conflict_text": a, "control_text": b}
    return None


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    rows = [json.loads(l) for l in Path("probes/triggers.jsonl").read_text().splitlines()]
    cache, jobs = {}, []
    for r in rows:
        if r["ws"] not in cache:
            msgs = load_msgs(r["ws"])
            cache[r["ws"]] = (load(r["ws"]), {m["msg_id"]: m for m in msgs})
        d, by_id = cache[r["ws"]]
        w = stale_value(d, by_id, r["ws"], r["fact_id"], r["value"], r["q_seq"])
        jobs.append((d, r, w, "stale" if w else "invented"))
    kinds = {}
    for j in jobs:
        kinds[j[3]] = kinds.get(j[3], 0) + 1
    print(f"{len(jobs)} probe positions; wrong value: {kinds}")
    if a.dry:
        return
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(make_one, jobs))
    out = [r for r in res if r]
    OUT.write_text("\n".join(json.dumps(r) for r in out) + "\n")
    points = []
    for r in out:
        for kind, text, gold in (("conflict", r["conflict_text"], "INTERVENE"), ("control", r["control_text"], "IGNORE")):
            points.append({"point_id": f"{r['probe_id']}#{kind}", "ws": r["ws"], "seq": r["q_seq"], "channel": r["channel"],
                           "thread": r["thread"], "kind": f"probe_{kind}", "plant_id": None, "gold_label": gold,
                           "virtual": {"speaker": r["speaker"], "text": text},
                           "evidence_groups": r["evidence_groups"], "fact_id": r["fact_id"], "current": r["current"],
                           "wrong": r["wrong"], "conflict_kind": r["conflict_kind"], "origin_form": r["origin_form"],
                           "bucket": r["bucket"]})
    POINTS.write_text(json.dumps(points, indent=0))
    print(f"-> {OUT}: {len(out)} pairs ({len(jobs) - len(out)} dropped); {POINTS}: {len(points)} points")
    for r in out[:3]:
        print(f"  [{r['conflict_kind']}] {r['entity']}: wrong={r['wrong']!r} current={r['current']!r}\n"
              f"    conflict: {r['conflict_text']}\n    control:  {r['control_text']}")


if __name__ == "__main__":
    main()
