"""Probe triggers: extra retrieval queries so each evidence form has enough n (3.5).

    python -m probes.make_triggers               # all workspaces -> probes/triggers.jsonl
    python -m probes.make_triggers --dry         # positions + counts only, no API calls

A probe trigger is a realistic message that mentions a fact's entity WITHOUT its value, imagined at a
later moment. It is used only as a proactive retrieval query; it is never inserted into the chat and
needs no label (the right answer is the fact's value in force at that moment).

Positions: for every origin evidence group, at the start and the middle of each LATER thread in which
its value is still current. If an evidence form still has < 12 probes, a third position (late in the
thread) is added for that form's groups.

Timing convention: a probe sits just before message q_seq. Memory and the window may use messages
with seq < q_seq (use window(msgs, q_seq - 1, channel)).

Evidence: the probed group (origin=True) plus every other group stating the same value of the same
fact before q_seq (restatements, origin=False), plus accepted audit restatements.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from memory.base import load_msgs
from sim.run_workspace import load, vpat

TRIGGER = """Write one short chat message from {PERSONA} ({ROLE}) in {CHANNEL} that mentions the
{ENTITY} ({ATTRIBUTE}) in passing (e.g. planning around it, asking about it) WITHOUT stating its value.
Keep it casual, under 30 words, in the voice of a busy teammate.
Return only the message text."""

WSS = ["ando", "anthropic", "openai", "xai"]
MIN_PER_FORM = 12
OUT = Path("probes/triggers.jsonl")


def fact_sets(d, ws, by_id):
    """fact_id -> sorted [(seq, value)] of every time the ledger sets it."""
    out = {}
    for f in d["facts"]:
        s = []
        for h in f["history"]:
            m = by_id.get(f"{ws}/{h['set_in']}/{h['turn']:03d}")
            if m:
                s.append((m["seq"], h["value"]))
        out[f["id"]] = sorted(s)
    return out


def positions(ws, extra_late_forms=frozenset()):
    d, msgs = load(ws), load_msgs(ws)
    by_id = {m["msg_id"]: m for m in msgs}
    groups = defaultdict(list)
    for m in msgs:
        if m["group"]:
            groups[m["group"]].append(m)
    sets = fact_sets(d, ws, by_id)
    threads = defaultdict(list)
    for m in msgs:
        threads[m["thread"]].append(m)
    audit = {}
    ap = Path(f"data/workspaces/{ws}/restatements.json")
    if ap.exists():
        plants = {json.loads(l)["plant_id"]: json.loads(l) for l in
                  Path(f"data/workspaces/{ws}/plants.jsonl").read_text().splitlines()}
        for pid, hits in json.loads(ap.read_text()).items():
            p = plants.get(pid, {})
            for h in hits:
                if h.get("verdict") == "accept" and p.get("fact_id"):
                    audit.setdefault((p["fact_id"], p["gold_value"]), []).append(h["msg_id"])

    rows = []
    for gid, gms in groups.items():
        g0 = gms[0]
        if not g0["group_origin"]:
            continue
        fact, value, form = g0["group_fact"], g0["group_value"], g0["group_form"]
        g_last = max(m["seq"] for m in gms)
        later_sets = [s for s, _ in sets.get(fact, []) if s > g_last]
        until = later_sets[0] if later_sets else 10 ** 9            # value current until replaced
        ev_channel = by_id[max(gms, key=lambda m: m["seq"])["msg_id"]]["channel"]
        for tid, tms in sorted(threads.items(), key=lambda kv: kv[1][0]["seq"]):
            main = [m for m in tms if not m["side"]] or tms
            if main[0]["seq"] <= g_last:                              # only threads that start later
                continue
            picks = [("start", main[0]), ("middle", main[len(main) // 2])]
            if form in extra_late_forms:
                picks.append(("late", main[(3 * len(main)) // 4]))
            for pos, anchor in picks:
                q = anchor["seq"]
                if q >= until:
                    continue
                ev = []
                for og, oms in groups.items():
                    o0 = oms[0]
                    if o0["group_fact"] == fact and o0["group_value"] == value and max(m["seq"] for m in oms) < q:
                        ev.append({"group": og, "form": o0["group_form"], "origin": og == gid,
                                   "msgs": [m["msg_id"] for m in sorted(oms, key=lambda m: m["seq"])]})
                for mid in audit.get((fact, value), []):
                    if by_id[mid]["seq"] < q:
                        ev.append({"group": f"{fact}@restate/{mid}", "form": "restatement", "origin": False,
                                   "msgs": [mid]})
                dist = q - g_last
                bucket = "cross" if anchor["channel"] != ev_channel else ("near" if dist < 15 else "far")
                rows.append({"probe_id": f"{ws}-{gid}-{tid}-{pos}", "ws": ws, "q_seq": q,
                             "anchor_msg": anchor["msg_id"], "channel": anchor["channel"], "thread": tid,
                             "position": pos, "fact_id": fact, "value": value,
                             "entity": d["_fact"][fact]["entity"], "attribute": d["_fact"][fact]["attribute"],
                             "evidence_groups": ev, "origin_group": gid, "origin_form": form,
                             "distance_msgs": dist, "bucket": bucket,
                             "speakers": sorted({m["speaker"] for m in main})})
    return d, rows


def write_text(d, row, tries=6):
    from sim.llm import complete
    model = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")
    rng = random.Random(row["probe_id"])
    pat = vpat(d, row["fact_id"], row["value"])
    for attempt in range(tries):
        sp = rng.choice(row["speakers"])
        per = d["_persona"][sp]
        prompt = (TRIGGER.replace("{PERSONA}", per["name"]).replace("{ROLE}", per["role"])
                  .replace("{CHANNEL}", row["channel"]).replace("{ENTITY}", row["entity"])
                  .replace("{ATTRIBUTE}", row["attribute"]))
        text = complete(None, prompt, model=model, max_tokens=120, seed=attempt).text.strip().strip('"')
        if text and not pat.search(text):
            return sp, text, attempt + 1
    return None, None, tries


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    per_ws = {ws: positions(ws) for ws in WSS}
    forms = Counter(r["origin_form"] for _, rows in per_ws.values() for r in rows)
    short = frozenset(f for f, n in forms.items() if n < MIN_PER_FORM)
    if short:
        print(f"forms under {MIN_PER_FORM} with start+middle: {sorted(short)} -> adding a 'late' position")
        per_ws = {ws: positions(ws, short) for ws in WSS}
    rows = [(d, r) for d, rs in per_ws.values() for r in rs]
    print("probes per origin form:", dict(Counter(r["origin_form"] for _, r in rows)))
    print("by bucket:", dict(Counter(r["bucket"] for _, r in rows)), f"| total {len(rows)}")
    if a.dry:
        return

    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda dr: write_text(*dr), rows))
    out, failed = [], 0
    for (d, r), (sp, text, n) in zip(rows, res):
        if text is None:
            failed += 1
            continue
        r = dict(r, speaker=sp, text=text, attempts=n)
        r.pop("speakers")
        out.append(r)
    OUT.write_text("\n".join(json.dumps(r) for r in out) + "\n")
    print(f"-> {OUT}: {len(out)} probes ({failed} dropped: value leaked in every attempt)")
    print("final per origin form:", dict(Counter(r["origin_form"] for r in out)))


if __name__ == "__main__":
    main()
