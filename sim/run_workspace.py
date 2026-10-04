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
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    for f in d["facts"]:
        assert "keys" in f, f"fact {f['id']} has no keys"
    expand_forms(d)
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


# ---------------------------------------------------------------- value / entity patterns
def _value_core(v: str) -> str:
    # "$12 per seat, agent actions metered" -> "$12"; "Amara Okafor (CIO)" -> "Amara Okafor"; "1,200 items" kept
    return v.split(", ")[0].split(" per ")[0].split(" (")[0].strip()


def value_regex(v: str, match: str | None = None) -> re.Pattern:
    """Regex that finds a value in text. A ledger `match:` overrides the derived pattern."""
    if match:
        return re.compile(match, re.I)
    alts = [rf"(?<!\w){re.escape(_value_core(v))}(?!\w)"]
    m = re.match(r"([A-Z][a-z]{2}) (\d{1,2})$", v)
    if m:  # "Sep 17" -> also "Sept 17", "September 17th", "9/17", "17th", "the 17"
        mon, day = m.group(1), m.group(2)
        num = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(mon) + 1
        alts += [rf"\b{mon}[a-z]*\.? {day}(st|nd|rd|th)?\b", rf"\b{num}/{day}\b",
                 rf"\b{day}(st|nd|rd|th)\b", rf"\bthe {day}\b"]
    return re.compile("|".join(alts), re.I)


def vpat(d, fact_id: str, value: str) -> re.Pattern:
    """Regex for one value of a fact, honoring the ledger's `match:` override."""
    h = next((h for h in d["_fact"][fact_id]["history"] if h["value"] == value), {})
    return value_regex(value, h.get("match"))


def keys_regex(keys) -> re.Pattern:
    """Regex for words that name a fact's entity (ledger `keys:`)."""
    return re.compile("|".join(re.escape(k) for k in keys), re.I)


# ---------------------------------------------------------------- evidence forms
def expand_forms(d) -> None:
    """Add each form's helper message (ask / setup / proposal / part 2) as an extra event
    in the thread where it belongs, and tag every fact statement with an evidence-group id."""
    threads = {t["id"]: t for t in d["threads"]}
    extra = []
    for t in d["threads"]:
        for e in t["events"]:
            if e["type"] not in ("establish", "update"):
                continue
            form = e.setdefault("form", "explicit")
            e["group"] = f"{e['fact']}@{t['id']}/{e['turn']:03d}"
            base = {"fact": e["fact"], "group": e["group"], "form": form,
                    "parent_thread": t["id"], "parent_turn": e["turn"]}
            if form in ("ellipsis", "reaction"):
                a = e["ask"]
                extra.append((t["id"], {**base, "type": "form_ask", "turn": a["turn"], "speaker": a["speaker"],
                                        "proposes_value": a.get("proposes_value", False),
                                        "for_reaction": form == "reaction", "emoji": e.get("emoji", "👍")}))
                e["reply_to"] = (t["id"], a["turn"])
            elif form == "correction":
                s = e["setup"]
                extra.append((t["id"], {**base, "type": "form_setup", "turn": s["turn"], "speaker": s["speaker"]}))
                e["reply_to"] = (t["id"], s["turn"])
            elif form == "cross_ref":
                r = e["ref"]
                extra.append((r["thread"], {**base, "type": "form_propose", "turn": r["turn"], "speaker": r["speaker"]}))
                e["reply_to"] = (r["thread"], r["turn"])
            elif form == "distributed":
                extra.append((t["id"], {**base, "type": "form_part2", "turn": e["part2_turn"],
                                        "speaker": e["speaker"], "part": e["parts"][1],
                                        "reply_to": (t["id"], e["turn"])}))
            elif form != "explicit":
                raise ValueError(f"{e['group']}: unknown form {form}")
    for tid, ev in extra:
        threads[tid]["events"].append(ev)


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
                "item_id": e.get("item"), "reply_to": None}
        cur, prev = value_at(d, e["fact"], tid, T) if f else (None, None)
        ent = f"{f['entity']} {f['attribute']}" if f else ""

        if typ in ("establish", "update"):
            v, old = value_at(d, e["fact"], tid, T, before=False)
            form, K, V = e["form"], keys_regex(f["keys"]), vpat(d, e["fact"], v)
            avoid = ", ".join(f["keys"])
            self_owner = v.lower() == name(d, sp).lower()   # owner facts where the speaker is the value
            meta.update(group=e["group"], group_fact=e["fact"], group_value=v, group_form=form,
                        group_origin=True, reply_to=e.get("reply_to"))
            h = next(h for h in f["history"] if h["set_in"] == tid and h["turn"] == T)
            reason = h.get("reason", "give a plausible reason")
            if form == "explicit" and typ == "establish":
                ins = f"State clearly, as a decision or announcement, that the {ent} is: {v}."
            elif form == "explicit":
                ins = f"Announce a change: the {ent} is now {v} (it was {old}). Reason: {reason}."
            elif form == "ellipsis" and not e["ask"].get("proposes_value"):
                ins = (f"Answer {name(d, e['ask']['speaker'])}'s question by volunteering yourself, in at most "
                       f"6 words. Do NOT name the thing or anyone. e.g. 'me', 'i'll grab it', 'on it'.")
                meta["forbid"] = [K, V]
            elif form == "ellipsis":
                ins = (f"Say yes to {name(d, e['ask']['speaker'])}'s question, in at most 6 words. Do NOT "
                       f"repeat the value or name the thing. e.g. 'yep, approved', 'confirmed, all yours'.")
                meta["forbid"] = [K, V]
            elif form == "reaction":
                meta["reaction"] = e.get("emoji", "👍")      # written without an LLM call (step 1.7)
                ins = f"(react {meta['reaction']} to {name(d, e['ask']['speaker'])}'s message)"
            elif form == "correction" and self_owner:
                ins = (f"{name(d, e['setup']['speaker'])} just said they're still on it. Take it over yourself "
                       f"instead. Reason: {reason}. At most 12 words. Do NOT name what it is or anyone. "
                       f"e.g. 'nah hand it to me, ...'")
                meta["forbid"] = [K, V]
            elif form == "correction":
                ins = (f"Correct the plan {name(d, e['setup']['speaker'])} just described: it should be {v}, "
                       f"not {old}. Reason: {reason}. At most 15 words. Do NOT name what it is "
                       f"(avoid: {avoid}). e.g. 'actually let's make that ...'")
                meta["forbid"], meta["require"] = [K], [V]
            elif form == "cross_ref":
                r = e["ref"]
                rday = next(t["day"] for t in d["threads"] if t["id"] == r["thread"])
                ins = (f"Say you're going with {name(d, r['speaker'])}'s suggestion from {rday} about the "
                       f"{f['entity']}, and that you're acting on it now. Do NOT state the value itself.")
                meta["forbid"] = [V]
            elif form == "distributed":
                ins = (f"State that the {ent} is: {e['parts'][0]}. Do NOT mention \"{e['parts'][1]}\" yet; "
                       f"you'll add that in a later message.")
        elif typ == "form_ask":
            v, _ = value_at(d, e["fact"], e["parent_thread"], e["parent_turn"], before=False)
            if e["proposes_value"]:
                ins = f"Ask, as a quick check, whether the {ent} is {v}. Name the {f['entity']} explicitly."
                meta["require"] = [keys_regex(f["keys"]), vpat(d, e["fact"], v)]
            else:
                ins = f"Ask who can take on / own the {f['entity']}. Name it explicitly. Don't suggest anyone."
                meta["require"] = [keys_regex(f["keys"])]
            if e["for_reaction"]:
                ins += f" Ask people to react {e['emoji']} if so."
            meta.update(group=e["group"], group_fact=e["fact"], group_value=v, group_form=e["form"],
                        group_origin=True)
        elif typ == "form_setup":
            v, _ = value_at(d, e["fact"], e["parent_thread"], e["parent_turn"], before=False)
            old, _ = value_at(d, e["fact"], e["parent_thread"], e["parent_turn"])
            if old.lower() == name(d, sp).lower():          # owner fact: the old owner is speaking
                ins = f"Say in passing that you're still on the {f['entity']} and will get to it soon."
            else:
                ins = f"Mention in passing, as part of a concrete plan, that the {ent} is {old}."
                meta["require"] = [vpat(d, e["fact"], old)]
            meta.update(group=e["group"], group_fact=e["fact"], group_value=v, group_form="correction",
                        group_origin=True)
        elif typ == "form_propose":
            v, _ = value_at(d, e["fact"], e["parent_thread"], e["parent_turn"], before=False)
            ins = (f"Float the idea, as a tentative suggestion, that the {ent} could be {v}. "
                   f"Make clear nothing is decided.")
            meta.update(group=e["group"], group_fact=e["fact"], group_value=v, group_form="cross_ref",
                        group_origin=True, require=[vpat(d, e["fact"], v)])
        elif typ == "form_part2":
            v, _ = value_at(d, e["fact"], e["parent_thread"], e["parent_turn"], before=False)
            ins = (f"Add one follow-up detail to your earlier message: {e['part']}. Start with 'and' or "
                   f"'also'. Do NOT name what it's about (avoid: {', '.join(f['keys'])}).")
            meta.update(group=e["group"], group_fact=e["fact"], group_value=v, group_form="distributed",
                        group_origin=True, reply_to=e["reply_to"], forbid=[keys_regex(f["keys"])])
        elif typ in ("contradiction", "stale_quote"):
            said = e.get("said_value") or prev
            known = any(h["value"] == said for h in f["history"])
            if known:
                meta["require"] = [vpat(d, e["fact"], said)]
            elif len(said.split()) <= 4:                    # invented short values like "$25M"
                meta["require"] = [value_regex(said)]
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
            meta.update(group=f"{e['fact']}@{tid}/{T:03d}r", group_fact=e["fact"], group_value=cur,
                        group_form="explicit", group_origin=False)
        elif typ == "answered_question":
            ins = f"{detail}. Ask the question only; do not include the answer."
            add(T + 1, {"speaker": e["answered_by"], **meta, "event_type": "answer",
                        "event_id": None, "reply_to": (tid, T),
                        "group": f"{e['fact']}@{tid}/{T + 1:03d}r", "group_fact": e["fact"],
                        "group_value": cur, "group_form": "explicit", "group_origin": False,
                        "instruction": f"Answer {name(d, sp)}'s question directly: the {ent} is {cur}."})
        elif typ == "decoy_self_correction":
            wrong = e.get("said_value") or prev
            ins = (f"Mention the {ent} in passing as \"{wrong}\" (a slip). "
                   f"Context: {detail}.")
            add(T + 1, {"speaker": sp, **meta, "event_type": "self_correction_fix", "event_id": None,
                        "reply_to": (tid, T),
                        "group": f"{e['fact']}@{tid}/{T + 1:03d}r", "group_fact": e["fact"],
                        "group_value": cur, "group_form": "explicit", "group_origin": False,
                        "instruction": f"Correct your previous message: the {ent} is actually {cur}. Keep it short (e.g. starts with '*' or 'sorry,')."})
        elif typ == "decoy_proposal":
            ins = f"{detail.split(';')[0]}. Phrase it as a tentative what-if question, not a decision."
            setter = f["history"][-1]["by"] if f else sp
            add(T + 1, {"speaker": setter, **meta, "event_type": "proposal_reply", "event_id": None,
                        "reply_to": (tid, T),
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
- Messages are short like real team chat: most are under 20 words, many are a quick fragment ("on it", "same", "lgtm"). Only about one in six runs longer, up to ~40 words. No sign-offs, no markdown headers, no greetings on every message.
- Stay in the speaker's voice and role. Do not narrate; write only what they type.
- Messages are numbered [n]. Reply with ONLY a JSON object:
  {{"speaker": "<person id>", "text": "<message>", "reply_to": <number of the one earlier message this depends on, or null (the usual case)>}}"""


def render(msgs) -> str:
    out = []
    for m in msgs:
        if m.get("kind") == "reaction":
            out.append(f"[{m['turn']}] ({m['speaker']} reacted {m['text']} to message {m.get('reply_to_turn')})")
        else:
            out.append(f"[{m['turn']}] {m['speaker']}: {m['text']}")
    return "\n".join(out) or "(no messages yet; you start the thread)"


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
        "Keep it under 20 words unless it truly needs more.",
        "Set reply_to ONLY if your message would be unclear without one specific earlier message (a direct answer, "
        "'yes'/'agreed' to a proposal, a follow-up to a question). Most messages just continue the conversation: use null.",
        "Never write any of these tracked values (refer to them indirectly, e.g. 'the sponsor', 'the discount', "
        "'the date'): " + "; ".join(tracked_terms(d)) + ".",
    ]
    if open_items:
        lines.append("Do not mention whether these are done or their status: " + "; ".join(open_items) + ".")
    if quiet_note:
        lines.append(quiet_note)
    return head + "\n".join(lines)


def tracked_terms(d) -> list[str]:
    """Short forms of every tracked value that is not a team member's name (for the filler prompt)."""
    persona_names = {p["name"].lower() for p in d["personas"]}
    out = []
    for f in d["facts"]:
        for h in f["history"]:
            core = _value_core(str(h["value"]))
            if core.lower() not in persona_names and core not in out:
                out.append(core)
    return out


# ---------------------------------------------------------------- tracked-value leak check
def leak_patterns(d) -> list[tuple[str, re.Pattern]]:
    persona_names = {p["name"].lower() for p in d["personas"]}
    pats = []
    for f in d["facts"]:
        for h in f["history"]:
            v = str(h["value"])
            if v.split(" (")[0].lower() in persona_names:
                continue  # owners are people; their names appear naturally
            pats.append((v, value_regex(v, h.get("match"))))
    return pats


# ---------------------------------------------------------------- generation
def stub(entry, recent, personas):
    sp = entry["speaker"] if entry else random.choice([p for p in personas if not recent or p != recent[-1]["speaker"]])
    return {"speaker": sp, "text": (f"[{entry['event_type']}] {entry['instruction'][:90]}" if entry else "[filler]")}


ATTEMPTS = 6   # forbid/require checks on scripted messages need a few more tries


def gen_message(d, thread, turn, recent, entry, quiet_note, open_items, args, leaks, allowed=None):
    """Returns (speaker, text, attempts_used, reply_turn). reply_turn is the filler writer's
    own reply_to (a turn number in `recent`), or None."""
    personas = list(allowed or d["_persona"])
    sysp = system_prompt(d)
    why = "no output"
    for attempt in range(ATTEMPTS):
        if args.dry_run:
            out = stub(entry, recent, personas)
        else:
            r = complete(sysp, user_prompt(d, thread, turn, recent, entry, quiet_note, open_items),
                         model=args.model, max_tokens=1000,
                         seed=args.seed * 100 + attempt)
            if r.stop_reason == "max_tokens":
                why = "hit max_tokens"
                continue
            try:
                out = parse_json(r.text)
            except ValueError:
                # the model sometimes mirrors the transcript format: "speaker: text"
                m = re.match(r"\s*(?:\[\d+\]\s*)?([a-z]+)\s*:\s*(.+)", r.text.strip(), re.S)
                if m and m.group(1) in d["_persona"]:
                    out = {"speaker": m.group(1), "text": m.group(2).strip()}
                elif entry and r.text.strip():
                    # scripted message: the speaker is fixed, so plain text is usable as is
                    out = {"speaker": entry["speaker"], "text": r.text.strip().strip('"')}
                else:
                    why = f"unparseable output: {r.text[:100]!r}"
                    continue
        sp, text = out.get("speaker"), str(out.get("text", "")).strip()
        if re.search(r"</?[a-zA-Z][\w:-]*[^>]*>", text) or text[:1] in "{<":
            why = f"markup instead of a message: {text[:80]!r}"
            continue
        if entry:
            sp = entry["speaker"]
        if sp not in d["_persona"] or not text or (allowed and sp not in allowed):
            why = f"bad speaker {sp!r} or empty text"
            continue
        if not entry and recent and sp == recent[-1]["speaker"]:
            why = f"{sp} spoke twice in a row"
            continue
        hit = next((v for v, p in leaks if p.search(text)), None) if not entry else None
        if hit:
            why = f"filler leaked tracked value {hit!r}: {text[:100]!r}"
            continue  # filler restated a tracked value; resample
        if entry and not args.dry_run:
            bad = next((p.pattern for p in entry.get("forbid", []) if p.search(text)), None)
            if bad:
                why = f"used a banned word /{bad}/: {text[:100]!r}"
                continue  # scripted message used a banned word (entity / value); resample
            miss = next((p.pattern for p in entry.get("require", []) if not p.search(text)), None)
            if miss:
                why = f"missing required /{miss}/: {text[:100]!r}"
                continue  # scripted message is missing a required entity / value; resample
        rt = out.get("reply_to")
        rt = rt if isinstance(rt, int) and any(m["turn"] == rt for m in recent[-8:]) else None
        return sp, text, attempt, rt
    raise RuntimeError(f"{thread['id']} turn {turn}: no valid message after {ATTEMPTS} attempts"
                       + (f"\n  instruction: {entry['instruction'][:160]}" if entry else "")
                       + f"\n  last rejection: {why}")


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
        if entry and "reaction" in entry:               # reactions cost no LLM call
            sp, text, attempts, rt = entry["speaker"], entry["reaction"], 0, None
        else:
            sp, text, attempts, rt = gen_message(d, thread, turn, msgs[-CONTEXT_MSGS:], entry, note,
                                                 open_items, args, leaks)
        ws, g = d["workspace"], entry or {}
        link = g.get("reply_to")                        # (thread, turn) scripted in the ledger
        reply_to = (f"{ws}/{link[0]}/{link[1]:03d}" if link else
                    f"{ws}/{tid}/{rt:03d}" if rt else None)
        row = {"msg_id": f"{ws}/{tid}/{turn:03d}", "thread": tid, "turn": turn,
               "day": thread["day"], "channel": thread["channel"], "speaker": sp, "text": text,
               "kind": "reaction" if "reaction" in g else "message",
               "reply_to": reply_to, "reply_to_turn": link[1] if link else rt,
               "thread_ts": None, "side": False,
               "event_type": g.get("event_type", "filler"), "event_id": g.get("event_id"),
               "fact_id": g.get("fact_id"), "item_id": g.get("item_id"),
               "group": g.get("group"), "group_fact": g.get("group_fact"),
               "group_value": g.get("group_value"), "group_form": g.get("group_form"),
               "group_origin": g.get("group_origin")}
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


# ---------------------------------------------------------------- channel structure
def run_side(d, thread, args, leaks, log):
    """Generate an unrelated side conversation for an `interleaved` thread."""
    s = thread["side"]
    fake = {**thread, "situation": s["situation"], "n_turns": s["n_msgs"]}
    note = ("This is a short side conversation about something unrelated to the team's work items. "
            f"Only {', '.join(name(d, p) for p in s['speakers'])} speak.")
    ws, tid, msgs = d["workspace"], thread["id"], []
    for k in range(1, s["n_msgs"] + 1):
        sp, text, attempts, rt = gen_message(d, fake, k, msgs[-CONTEXT_MSGS:], None, note, [], args, leaks,
                                             allowed=s["speakers"])
        row = {"msg_id": f"{ws}/{tid}/s{k:02d}", "thread": tid, "turn": k,
               "day": thread["day"], "channel": thread["channel"], "speaker": sp, "text": text,
               "kind": "message", "reply_to": f"{ws}/{tid}/s{rt:02d}" if rt else None,
               "reply_to_turn": rt, "thread_ts": None, "side": True,
               "event_type": "side", "event_id": None, "fact_id": None, "item_id": None,
               "group": None, "group_fact": None, "group_value": None, "group_form": None,
               "group_origin": None}
        msgs.append(row)
        if attempts:
            log.append(f"{row['msg_id']}: {attempts} resample(s)")
        print(f"{row['msg_id']}  {sp:>7}: {text}")
    return msgs


def interleave(main, side, thread, rng):
    """Insert side messages between main messages, at most one per gap. Scripted pairs
    (question -> answer etc.) stay adjacent, except events marked `gap: true`, which are
    forced to get a side message between helper and answer."""
    gap_turns = {e["turn"] for e in thread["events"] if e.get("gap")}
    glued = {m["msg_id"] for i, m in enumerate(main) if i and m["group"] and m["turn"] not in gap_turns
             and m["reply_to"] == main[i - 1]["msg_id"]}
    slots = [i for i in range(1, len(main)) if main[i]["msg_id"] not in glued]   # insert before main[i]
    forced = [i for i in slots if main[i]["turn"] in gap_turns]
    others = [i for i in slots if i not in forced]
    k = max(0, min(len(others), len(side) - len(forced)))
    where = set(forced) | set(rng.sample(others, k))
    out, si = [], 0
    for i, m in enumerate(main):
        if i in where and si < len(side):
            out.append(side[si]); si += 1
        out.append(m)
    return out + side[si:]


def apply_threading(d, rows):
    """In `threaded` threads, every same-thread reply sits under its root, like a Slack thread.
    Reactions keep their target link; cross-thread references stay unthreaded."""
    by_id = {r["msg_id"]: r for r in rows}
    struct = {t["id"]: t.get("structure", "flat") for t in d["threads"]}
    for r in rows:
        if struct[r["thread"]] != "threaded" or not r["reply_to"] or r["kind"] == "reaction":
            continue
        p = by_id.get(r["reply_to"])
        if not p or p["thread"] != r["thread"]:
            continue
        while p["reply_to"] in by_id and by_id[p["reply_to"]]["thread"] == r["thread"]:
            p = by_id[p["reply_to"]]
        r["thread_ts"] = p["msg_id"]


# ---------------------------------------------------------------- plants
def build_plants(d, msgs) -> list[dict]:
    by_id = {m["msg_id"]: i for i, m in enumerate(msgs)}
    def mid(thread, turn):
        return f"{d['workspace']}/{thread}/{turn:03d}"

    # evidence groups: every message set that states a fact's value (msgs are in seq order)
    groups: dict[str, list[int]] = defaultdict(list)
    for i, m in enumerate(msgs):
        if m.get("group"):
            groups[m["group"]].append(i)
    head = {g: msgs[ix[0]] for g, ix in groups.items()}
    struct = {t["id"]: t.get("structure", "flat") for t in d["threads"]}

    plants = []
    for t in d["threads"]:
        for e in t["events"]:
            if not e.get("id") or (e["type"] not in PLANT_TYPES and "decoy" not in e["type"]
                                   and e["type"] not in ("banter", "sensitive", "answered_question")):
                continue
            # answered_question / decoy_self_correction are only IGNORE once the follow-up exists
            # (the answer, the "*24th, sorry"), so the decision point is that follow-up message
            follow = e["type"] in ("answered_question", "decoy_self_correction")
            trig = mid(t["id"], e["turn"] + 1 if follow else e["turn"])
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
                cands = [g for g, ix in groups.items()
                         if head[g]["group_fact"] == e["fact"] and head[g]["group_value"] == cur
                         and max(ix) < ti]
                if cands:
                    origin = next((g for g in cands if head[g]["group_origin"]), None)
                    p["evidence_groups"] = [{"group": g, "form": head[g]["group_form"],
                                             "origin": bool(head[g]["group_origin"]),
                                             "msgs": [msgs[i]["msg_id"] for i in groups[g]]} for g in cands]
                    p["evidence_msgs"] = [msgs[i]["msg_id"] for i in groups[origin]] if origin else []
                    p["evidence_form"] = head[origin]["group_form"] if origin else "explicit"
                    p["restated"] = len(cands) > 1
                    o = groups[origin][0] if origin else groups[cands[0]][0]
                    p["structure"] = struct[msgs[o]["thread"]]
                    ev_idx = max(max(groups[g]) for g in cands)      # nearest evidence message
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
                        p["evidence_groups"] = [{"group": e["item"], "form": "explicit", "origin": True,
                                                 "msgs": [oid]}]
                        p["evidence_form"], p["restated"] = "explicit", False
                        p["structure"] = struct[o["thread"]]
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
    ap.add_argument("--workers", type=int, default=8,
                    help="threads and side conversations generated in parallel (1 = sequential)")
    args = ap.parse_args()
    random.seed(args.seed)

    d = load(args.ws)
    want = set(args.threads.split(",")) if args.threads else None
    leaks, log = leak_patterns(d), []

    out = Path(f"data/workspaces/{args.ws}{'_dryrun' if args.dry_run else ''}")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "messages.jsonl"
    per: dict[str, list[dict]] = defaultdict(list)
    if want and path.exists():                       # keep the threads we are not regenerating
        for r in map(json.loads, path.read_text().splitlines()):
            if r["thread"] not in want:
                per[r["thread"]].append(r)
    # Threads are independent (each starts fresh; cross-thread links come from the ledger), so
    # every thread and every side conversation is generated in parallel. Within one, messages
    # stay sequential because each is written with the previous ones as context.
    todo = [t for t in d["threads"] if not want or t["id"] in want]
    jobs = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        for t in todo:
            jobs[ex.submit(run_thread, d, t, args, leaks, log)] = (t, "main")
            if t.get("structure") == "interleaved":
                jobs[ex.submit(run_side, d, t, args, leaks, log)] = (t, "side")
        done, errors = defaultdict(dict), []
        for fut in as_completed(jobs):
            t, part = jobs[fut]
            try:
                done[t["id"]][part] = fut.result()
            except Exception as exc:                  # keep going; report all failures at the end
                errors.append(f"{t['id']} ({part}): {exc}")
    for t in todo:
        got = done.get(t["id"], {})
        if "main" not in got or (t.get("structure") == "interleaved" and "side" not in got):
            continue                                  # failed thread: keep its previous rows, if any
        rows = got["main"]
        if "side" in got:                             # per-thread rng: same result in any run order
            rows = interleave(rows, got["side"], t, random.Random(f"{args.seed}:{t['id']}"))
        per[t["id"]] = rows
    msgs = [r for t in d["threads"] for r in per[t["id"]]]
    apply_threading(d, msgs)
    for k, r in enumerate(msgs):
        r["seq"] = k                                 # the only ordering downstream code should use

    path.write_text("".join(json.dumps(m, ensure_ascii=False) + "\n" for m in msgs))
    plants = build_plants(d, msgs)
    (out / "plants.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in plants))
    print(f"\nwrote {len(msgs)} messages, {len(plants)} plants/decoys -> {out}/")
    if errors:
        print(f"\n{len(errors)} thread(s) FAILED and were not written (rerun them with --threads):")
        for e in errors:
            print("  ", e)
    for line in log:
        print("  ", line)
    if USAGE:
        print("usage:", {m: dict(v) for m, v in USAGE.items()})
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
