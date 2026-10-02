"""Expand a workspace ledger (world/ws_<name>.yaml) into chat messages and plants.

One LLM call per message. Event turns are scripted from the ledger with the exact
value to say; every other turn is filler written in character, with tracked values
withheld so filler can't restate them.

  python -m sim.run_workspace --ws ando                # all threads
  python -m sim.run_workspace --ws ando --threads t1   # just t1 (for reading)
  python -m sim.run_workspace --ws ando --dry-run      # no API calls, stub text

Writes data/workspaces/<ws>/messages.jsonl and plants.jsonl.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
from pathlib import Path

import yaml

from sim.llm import USAGE, complete, parse_json

CONTEXT_MSGS = 20     # recent messages shown to the writer
QUIET_AFTER = 2       # turns after an INTERVENE plant in which nobody may react to it
WINDOW = 15           # judge window; plants with evidence inside it are "near"

PLANT_TYPES = {"contradiction", "stale_quote", "repeat_question", "deadline_passed",
               "commitment", "pending_decision"}


# ---------------------------------------------------------------- ledger helpers
def load(ws: str) -> dict:
    d = yaml.safe_load(Path(f"world/ws_{ws}.yaml").read_text())
    d["_persona"] = {p["id"]: p for p in d["personas"]}
    d["_fact"] = {f["id"]: f for f in d["facts"]}
    d["_item"] = {i["id"]: i for i in d.get("open_items", [])}
    order, idx = {}, 0
    for t in d["threads"]:
        order[t["id"]] = idx
        idx += 1
    d["_thread_order"] = order
    return d


def pos(d, thread, turn):
    """Sortable position of (thread, turn) in the workspace."""
    return (d["_thread_order"][thread], turn)


def value_at(d, fact_id, thread, turn, before=True):
    """The fact's value in force at (thread, turn); `before` excludes a change made at that very turn."""
    cur = prev = None
    for h in d["_fact"][fact_id]["history"]:
        p = pos(d, h["set_in"], h["turn"])
        if p < pos(d, thread, turn) or (not before and p == pos(d, thread, turn)):
            prev, cur = cur, h["value"]
    return cur, prev


def name(d, pid):
    return d["_persona"][pid]["name"]


# ---------------------------------------------------------------- script for each turn
def build_schedule(d, thread) -> dict[int, dict]:
    """turn -> scripted instruction (speaker, instruction, event metadata)."""
    sched: dict[int, dict] = {}
    tid = thread["id"]

    def add(turn, entry):
        if turn in sched:
            raise ValueError(f"{tid} turn {turn}: two scripted events collide")
        sched[turn] = entry

    for e in thread["events"]:
        T, sp, typ = e["turn"], e.get("speaker"), e["type"]
        f = d["_fact"].get(e.get("fact"))
        it = d["_item"].get(e.get("item"))
        detail = e.get("detail", "")
        meta = {"event_type": typ, "event_id": e.get("id"), "fact_id": e.get("fact"),
                "item_id": e.get("item")}
        cur, prev = value_at(d, e["fact"], tid, T) if f else (None, None)
        ent = f"{f['entity']} {f['attribute']}" if f else ""

        if typ == "establish":
            v, _ = value_at(d, e["fact"], tid, T, before=False)
            ins = f"State clearly, as a decision or announcement, that the {ent} is: {v}."
        elif typ == "update":
            v, old = value_at(d, e["fact"], tid, T, before=False)
            h = next(h for h in f["history"] if h["set_in"] == tid and h["turn"] == T)
            ins = (f"Announce a change: the {ent} is now {v} (it was {old}). "
                   f"Reason: {h.get('reason', 'give a plausible reason')}.")
        elif typ in ("contradiction", "stale_quote"):
            said = e.get("said_value") or prev
            ins = (f"{detail}. Use the value \"{said}\" naturally and confidently, as if it were "
                   f"correct. Do not hedge, and do not mention any other value for the {ent}.")
        elif typ == "repeat_question":
            ins = f"{detail}. Ask about the {ent} as a genuine question. Do not include any answer."
        elif typ in ("commitment", "pending_decision"):
            kind = "commit to" if typ == "commitment" else "say the team will decide"
            ins = (f"{detail}. Make it explicit: {kind} \"{it['what']}\", with the check point "
                   f"\"{it['check_point']}\".")
        elif typ == "resolve":
            ins = f"{detail}. Say clearly that this is done: {it['what']}."
        elif typ in ("deadline_passed", "decoy_resolved_before_checkpoint"):
            ins = (f"Write a normal message about the thread's situation ({detail}). "
                   f"Do NOT mention anything about: {it['what']}.")
        elif typ == "decoy_legit_change_quote":
            ins = f"{detail}. Mention the current {ent}, {cur}, as a matter of fact."
        elif typ == "answered_question":
            ins = f"{detail}. Ask the question only; do not include the answer."
            add(T + 1, {"speaker": e["answered_by"], **meta, "event_type": "answer",
                        "event_id": None,
                        "instruction": f"Answer {name(d, sp)}'s question directly: the {ent} is {cur}."})
        elif typ == "decoy_self_correction":
            wrong = e.get("said_value") or prev
            ins = (f"Mention the {ent} in passing as \"{wrong}\" (a slip). "
                   f"Context: {detail}.")
            add(T + 1, {"speaker": sp, **meta, "event_type": "self_correction_fix", "event_id": None,
                        "instruction": f"Correct your previous message: the {ent} is actually {cur}. Keep it short (e.g. starts with '*' or 'sorry,')."})
        elif typ == "decoy_proposal":
            ins = f"{detail.split(';')[0]}. Phrase it as a tentative what-if question, not a decision."
            setter = f["history"][-1]["by"] if f else sp
            add(T + 1, {"speaker": setter, **meta, "event_type": "proposal_reply", "event_id": None,
                        "instruction": f"Briefly turn down {name(d, sp)}'s suggestion and keep the current plan. Do not restate any date, number or value."})
        else:  # banter, sensitive, similar_entity_decoy, ...
            ins = detail
        add(T, {"speaker": sp, "instruction": ins, **meta})
    return sched


# ---------------------------------------------------------------- prompts
def system_prompt(d) -> str:
    people = "\n".join(f"- {p['id']} ({p['name']}): {p['role']}. Style: {p['style']}."
                       for p in d["personas"])
    rules = "\n".join(f"- {r}" for r in d.get("filler_rules", []))
    return f"""You write a realistic workplace chat, one message at a time, for a research dataset.

Company: {d['company'].strip()}

People:
{people}

Rules:
{rules}
- Messages are short like real chat: usually one or two sentences, sometimes a fragment. No sign-offs, no markdown headers.
- Stay in the speaker's voice and role. Do not narrate; write only what they type.
- Reply with ONLY a JSON object: {{"speaker": "<person id>", "text": "<message>"}}"""


def render(msgs) -> str:
    return "\n".join(f"{m['speaker']}: {m['text']}" for m in msgs) or "(no messages yet; you start the thread)"


def user_prompt(d, thread, turn, recent, entry, quiet_note, open_items) -> str:
    phase = ("opening the thread" if turn == 1 else
             "wrapping up the thread" if turn > thread["n_turns"] - 4 else "middle of the thread")
    head = (f"Channel {thread['channel']}, {thread['day']}. Situation: {thread['situation']}\n"
            f"Message {turn} of {thread['n_turns']} ({phase}).\n\nRecent messages (oldest first):\n"
            f"{render(recent)}\n\n")
    if entry:
        return head + (f"Write the next message, from {name(d, entry['speaker'])} "
                       f"(id: {entry['speaker']}). It must do this:\n{entry['instruction']}\n"
                       f"Keep it natural for this conversation.")
    last = recent[-1]["speaker"] if recent else None
    lines = [
        "Write the next message. Pick whoever would naturally speak next"
        + (f" (not {last}, who just spoke)" if last else "") + ".",
        "It moves the situation forward with concrete but invented details (tasks, bugs, ideas, customer questions).",
        "Do not state any specific dates, deadlines, prices, amounts, counts, versions or thresholds that appear in earlier messages.",
        "Do not make new commitments with deadlines, and do not announce decisions.",
    ]
    if open_items:
        lines.append("Do not mention whether these are done or their status: " + "; ".join(open_items) + ".")
    if quiet_note:
        lines.append(quiet_note)
    return head + "\n".join(lines)


# ---------------------------------------------------------------- tracked-value leak check
def leak_patterns(d) -> list[tuple[str, re.Pattern]]:
    persona_names = {p["name"].lower() for p in d["personas"]}
    pats = []
    for f in d["facts"]:
        for h in f["history"]:
            v = str(h["value"])
            if v.split(" (")[0].lower() in persona_names:
                continue  # owners are people; their names appear naturally
            core = re.escape(v.split(",")[0].split(" per ")[0].strip())
            alts = [core]
            m = re.match(r"([A-Z][a-z]{2}) (\d{1,2})$", v)
            if m:  # "Sep 17" -> also "17th", "the 17"
                alts += [rf"\b{m.group(2)}(st|nd|rd|th)\b", rf"\bthe {m.group(2)}\b"]
            pats.append((v, re.compile("|".join(alts), re.I)))
    return pats


# ---------------------------------------------------------------- generation
def stub(entry, recent, personas):
    sp = entry["speaker"] if entry else random.choice([p for p in personas if not recent or p != recent[-1]["speaker"]])
    return {"speaker": sp, "text": (f"[{entry['event_type']}] {entry['instruction'][:90]}" if entry else "[filler]")}


def gen_message(d, thread, turn, recent, entry, quiet_note, open_items, args, leaks):
    personas = list(d["_persona"])
    sysp = system_prompt(d)
    for attempt in range(4):
        if args.dry_run:
            out = stub(entry, recent, personas)
        else:
            r = complete(sysp, user_prompt(d, thread, turn, recent, entry, quiet_note, open_items),
                         model=args.model, max_tokens=1000,
                         seed=args.seed * 100 + attempt)
            if r.stop_reason == "max_tokens":
                continue
            try:
                out = parse_json(r.text)
            except ValueError:
                # the model sometimes mirrors the transcript format: "speaker: text"
                m = re.match(r"\s*([a-z]+)\s*:\s*(.+)", r.text.strip(), re.S)
                if not m:
                    continue
                out = {"speaker": m.group(1), "text": m.group(2).strip()}
        sp, text = out.get("speaker"), str(out.get("text", "")).strip()
        if entry:
            sp = entry["speaker"]
        if sp not in d["_persona"] or not text:
            continue
        if not entry and recent and sp == recent[-1]["speaker"]:
            continue
        if not entry and any(p.search(text) for _, p in leaks):
            continue  # filler restated a tracked value; resample
        return sp, text, attempt
    raise RuntimeError(f"{thread['id']} turn {turn}: no valid message after 4 attempts")


def run_thread(d, thread, args, leaks, log):
    sched = build_schedule(d, thread)
    tid, msgs = thread["id"], []
    quiet_until, quiet_note = 0, ""
    for turn in range(1, thread["n_turns"] + 1):
        entry = sched.get(turn)
        # open items opened earlier and not yet resolved: filler must not touch their status
        open_items = [i["what"] for i in d["_item"].values()
                      if pos(d, i["opened_in"]["thread"], i["opened_in"]["turn"]) < pos(d, tid, turn)]
        note = quiet_note if turn <= quiet_until else ""
        sp, text, attempts = gen_message(d, thread, turn, msgs[-CONTEXT_MSGS:], entry, note,
                                         open_items, args, leaks)
        row = {"msg_id": f"{d['workspace']}/{tid}/{turn:03d}", "thread": tid, "turn": turn,
               "day": thread["day"], "channel": thread["channel"], "speaker": sp, "text": text,
               "event_type": entry["event_type"] if entry else "filler",
               "event_id": entry.get("event_id") if entry else None,
               "fact_id": entry.get("fact_id") if entry else None,
               "item_id": entry.get("item_id") if entry else None}
        msgs.append(row)
        if attempts:
            log.append(f"{row['msg_id']}: {attempts} resample(s)")
        ev = next((e for e in thread["events"] if e["turn"] == turn), None)
        if ev and ev.get("gold_label") == "INTERVENE":
            quiet_until = turn + QUIET_AFTER
            quiet_note = (f"Nobody reacts to, corrects or answers {name(d, sp)}'s message \"{text[:120]}\". "
                          f"Talk about something else.")
        print(f"{row['msg_id']}  {sp:>7}: {text}")
    return msgs


# ---------------------------------------------------------------- plants
def build_plants(d, msgs) -> list[dict]:
    by_id = {m["msg_id"]: i for i, m in enumerate(msgs)}
    def mid(thread, turn):
        return f"{d['workspace']}/{thread}/{turn:03d}"

    # every message that states a fact's then-current value
    statements: dict[str, list[tuple[int, str]]] = {}
    for i, m in enumerate(msgs):
        if m["fact_id"] and m["event_type"] in ("establish", "update", "decoy_legit_change_quote",
                                                 "answer", "self_correction_fix"):
            statements.setdefault(m["fact_id"], []).append((i, m["msg_id"]))

    plants = []
    for t in d["threads"]:
        for e in t["events"]:
            if not e.get("id") or (e["type"] not in PLANT_TYPES and "decoy" not in e["type"]
                                   and e["type"] not in ("banter", "sensitive", "answered_question")):
                continue
            trig = mid(t["id"], e["turn"])
            if trig not in by_id:
                continue  # thread not generated in this run
            ti = by_id[trig]
            p = {"plant_id": e["id"], "kind": "plant" if e["id"].split("-")[-1].startswith("p") else "decoy",
                 "type": e["type"], "trigger_msg": trig, "gold_label": e["gold_label"],
                 "severity": e["severity"], "fact_id": e.get("fact"), "item_id": e.get("item")}
            ev_idx = None
            if e.get("fact"):
                f = d["_fact"][e["fact"]]
                cur, prev = value_at(d, e["fact"], t["id"], e["turn"])
                p["gold_value"] = cur
                if e["type"] == "stale_quote":
                    p["stale_value"] = e.get("said_value") or prev
                if e["type"] == "contradiction":
                    p["said_value"] = e["said_value"]
                p["probe"] = f"What is the current {f['attribute']} of {f['entity']}?"
                prior = [s for s in statements.get(e["fact"], []) if s[0] < ti]
                if prior:
                    ev_idx = prior[-1][0]
                    p["evidence_msgs"] = [prior[-1][1]]
            elif e.get("item"):
                it = d["_item"][e["item"]]
                o = it["opened_in"]
                oid = mid(o["thread"], o["turn"])
                p["gold_value"] = f"{name(d, it['owner'])}: {it['what']} (check point {it['check_point']})"
                if e["type"] in ("commitment", "pending_decision"):
                    p["probe"] = f"What did {name(d, it['owner'])} commit to, and by when?"
                else:
                    p["probe"] = f"Is this done: {it['what']}?"
                    p["gold_value"] = "not done" if not it.get("resolved") else "done"
                    if oid in by_id:
                        ev_idx = by_id[oid]
                        p["evidence_msgs"] = [oid]
            if ev_idx is not None and p["kind"] == "plant" and e["type"] not in ("commitment", "pending_decision"):
                dist = ti - ev_idx
                same = msgs[ev_idx]["thread"] == t["id"]
                p["distance_msgs"] = dist
                p["bucket"] = "near" if dist < WINDOW else ("far" if same else "cross")
                if e.get("bucket") and e["bucket"] != p["bucket"]:
                    print(f"note: {e['id']} planned {e['bucket']}, generated {p['bucket']} (dist {dist})")
            plants.append(p)
    return plants


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", required=True)
    ap.add_argument("--threads", help="comma-separated thread ids (default: all)")
    ap.add_argument("--model", default=os.environ.get("SIM_MODEL"))
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true", help="no API calls; stub text")
    args = ap.parse_args()
    random.seed(args.seed)

    d = load(args.ws)
    want = set(args.threads.split(",")) if args.threads else None
    leaks, log, msgs = leak_patterns(d), [], []
    for t in d["threads"]:
        if want and t["id"] not in want:
            continue
        msgs += run_thread(d, t, args, leaks, log)

    out = Path(f"data/workspaces/{args.ws}{'_dryrun' if args.dry_run else ''}")
    out.mkdir(parents=True, exist_ok=True)
    (out / "messages.jsonl").write_text("".join(json.dumps(m) + "\n" for m in msgs))
    plants = build_plants(d, msgs)
    (out / "plants.jsonl").write_text("".join(json.dumps(p) + "\n" for p in plants))
    print(f"\nwrote {len(msgs)} messages, {len(plants)} plants/decoys -> {out}/")
    for line in log:
        print("  ", line)
    if USAGE:
        print("usage:", {m: dict(v) for m, v in USAGE.items()})


if __name__ == "__main__":
    main()
