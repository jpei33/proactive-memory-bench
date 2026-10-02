"""Check a generated workspace against its ledger.

    python -m world.verify --ws ando                 # data/workspaces/ando
    python -m world.verify --ws ando --dir data/workspaces/ando_dryrun

Checks
  1. links:       every reply_to points to an earlier message
  2. forms:       each fact statement obeys its evidence form (banned / required words,
                  right number of messages, linked to its helper, cross_ref spans threads)
  3. plants:      the trigger says the planted value; nothing restates the gold value in
                  plain words between the evidence and the trigger
  4. gaps:        events marked `gap: true` really have a side message inside the gap
Prints form / bucket counts, then every failure. Exit code 1 if anything failed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sim.run_workspace import keys_regex, load, vpat

STOP = set("the a an of to on in for is are and or with at by be it this that as from".split())


def loose_has(text: str, value: str) -> bool:
    """At least half of the value's content words appear in the text (for long planted values)."""
    words = [w for w in re.findall(r"[\w$%@.,]+", value.lower()) if len(w) > 2 and w not in STOP]
    return not words or sum(w in text.lower() for w in words) / len(words) >= 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", required=True)
    ap.add_argument("--dir", help="workspace output dir (default data/workspaces/<ws>)")
    a = ap.parse_args()
    d = load(a.ws)
    base = Path(a.dir or f"data/workspaces/{a.ws}")
    msgs = [json.loads(l) for l in (base / "messages.jsonl").read_text().splitlines()]
    plants = [json.loads(l) for l in (base / "plants.jsonl").read_text().splitlines()]
    by_id = {m["msg_id"]: m for m in msgs}
    people = {p["name"].lower(): p["id"] for p in d["personas"]}
    fails: list[str] = []

    def bad(mid, why):
        fails.append(f"{mid}: {why}")

    # 1. links point backwards
    for m in msgs:
        if m["reply_to"] and (m["reply_to"] not in by_id or by_id[m["reply_to"]]["seq"] >= m["seq"]):
            bad(m["msg_id"], f"reply_to {m['reply_to']} missing or not earlier")

    # 2. each origin evidence group obeys its form
    groups: dict[str, list[dict]] = defaultdict(list)
    for m in msgs:
        if m["group"] and m["group_origin"]:
            groups[m["group"]].append(m)
    for g, ms in groups.items():
        ms.sort(key=lambda m: m["seq"])
        first, last = ms[0], ms[-1]
        f = d["_fact"][first["group_fact"]]
        form, value = first["group_form"], first["group_value"]
        K, V = keys_regex(f["keys"]), vpat(d, f["id"], value)
        owner = people.get(value.lower())            # value is a person: the answer is *who* speaks
        expect = 1 if form == "explicit" else 2
        if len(ms) != expect:
            bad(g, f"{form} statement has {len(ms)} messages, expected {expect}")
            continue
        if form != "explicit" and last["reply_to"] != first["msg_id"]:
            bad(last["msg_id"], f"not linked to its helper {first['msg_id']}")
        if form == "explicit" and not V.search(last["text"]):
            bad(last["msg_id"], f"explicit statement lacks the value '{value}'")
        if form == "ellipsis":
            if K.search(last["text"]) or V.search(last["text"]):
                bad(last["msg_id"], "ellipsis answer names the entity or the value")
            if not K.search(first["text"]):
                bad(first["msg_id"], "ellipsis question doesn't name the entity")
            if owner and last["speaker"] != owner:
                bad(last["msg_id"], f"owner answer should come from {owner}")
        if form == "reaction":
            if last["kind"] != "reaction":
                bad(last["msg_id"], "reaction statement is not a reaction row")
            if not K.search(first["text"]):
                bad(first["msg_id"], "reacted-to message doesn't name the entity")
        if form == "correction":
            if K.search(last["text"]):
                bad(last["msg_id"], "correction names the entity")
            if owner:                                 # "hand it to me": the speaker is the value
                if last["speaker"] != owner:
                    bad(last["msg_id"], f"self-assignment should come from {owner}")
                if V.search(last["text"]):
                    bad(last["msg_id"], "self-assignment names the new owner")
            elif not V.search(last["text"]):
                bad(last["msg_id"], f"correction lacks the new value '{value}'")
        if form == "cross_ref":
            if V.search(last["text"]):
                bad(last["msg_id"], "adoption restates the value")
            if not V.search(first["text"]):
                bad(first["msg_id"], "proposal lacks the value")
            if first["thread"] == last["thread"]:
                bad(g, "cross_ref proposal and adoption are in the same thread")
        if form == "distributed" and K.search(last["text"]):
            bad(last["msg_id"], "part 2 names the entity")

    # 3. plants: trigger says the planted thing; nothing restates the gold value in between
    for p in plants:
        t = by_id.get(p["trigger_msg"])
        if t is None:
            bad(p["plant_id"], f"trigger {p['trigger_msg']} missing")
            continue
        said = p.get("said_value") or p.get("stale_value")
        if p["type"] in ("contradiction", "stale_quote") and said and not loose_has(t["text"], said):
            bad(t["msg_id"], f"{p['plant_id']} trigger doesn't say '{said}'")
        if (p["kind"] == "plant" and p.get("fact_id") and p.get("evidence_groups")
                and p["gold_value"].lower() not in people):       # names appear naturally in chat
            V = vpat(d, p["fact_id"], p["gold_value"])
            last_ev = max(by_id[i]["seq"] for g in p["evidence_groups"] for i in g["msgs"])
            for m in msgs[last_ev + 1: t["seq"]]:
                if m["event_type"] in ("filler", "side") and V.search(m["text"]):
                    bad(m["msg_id"], f"restates '{p['gold_value']}' before {p['plant_id']}")

    # 4. forced gaps really have a side message inside
    for th in d["threads"]:
        for e in th["events"]:
            if e.get("gap") and e.get("group") in groups:
                ms = sorted(groups[e["group"]], key=lambda m: m["seq"])
                if len(ms) == 2 and not any(m["side"] for m in msgs[ms[0]["seq"] + 1: ms[1]["seq"]]):
                    bad(e["group"], "gap: true but no side message inside the gap")

    # report
    fp = [p for p in plants if p["kind"] == "plant" and p.get("fact_id") and p["gold_label"] == "INTERVENE"]
    print(f"{a.ws}: {len(msgs)} messages ({sum(m['side'] for m in msgs)} side, "
          f"{sum(m['kind'] == 'reaction' for m in msgs)} reactions, "
          f"{sum(bool(m['reply_to']) for m in msgs)} with reply_to, {sum(bool(m['thread_ts']) for m in msgs)} threaded)")
    print("fact plants by form:", dict(Counter(p.get("evidence_form") for p in fp)),
          "| restated:", sum(p.get("restated", False) for p in fp), "of", len(fp))
    print("plant buckets:", dict(Counter(p.get("bucket") for p in plants if p["kind"] == "plant" and p.get("bucket"))))
    print("\n".join(fails) if fails else "0 failures")
    if fails:
        print(f"\n{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
