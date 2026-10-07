"""Build the private 'real' workspace from the labeled real-chat corpus (Step 1 of the 3-way plan).

    python -m memory.real_ws            # -> data/real/workspace/messages.jsonl + build_report.json

Input: data/real/candidates_claude_labeled.csv, one row per decision point (50 threads from 10
conversations). Each thread = prior_context + new_message; every message is a line
"M<nn> | <ISO timestamp> | <Speaker>: <text>" (text may span several lines).

Output uses the simulated workspaces' message schema, so every chunker, retriever and the judge
work unchanged (memory.base.load_msgs("real")):
  channel  = "#" + conversation_ref   (threads of one conversation share a channel, merged by time;
                                        the 15-message window and D's per-channel segmentation see
                                        the whole conversation, as in a real channel)
  thread   = thread_ref;  thread_ts = msg_id of the thread's first message (Slack-style root)
  reply_to = None (the export has no reply links)
  is_agent = speaker starts with "Agent"   (extra field: the human-vs-agent view for arm 1)
  ts       = original timestamp (extra field); day = "Wed Aug 26" like the simulated data
Messages that appear in two threads (same conversation, timestamp, speaker, text) are kept once.

PRIVATE: everything written here stays under data/real/ (git-ignored). Do not move it to
data/workspaces/, which is tracked, and do not add "real" to any --all list.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

SRC = Path("data/real/candidates_claude_labeled.csv")
OUT = Path("data/real/workspace")
LINE = re.compile(r"(?m)^(M\d+) \| (\d{4}-\d\d-\d\dT[\d:.]+Z) \| ([^:\n]+?): ")


def parse_thread(text: str) -> list[dict]:
    """'M01 | ts | Speaker: text...' blocks -> [{local_id, ts, speaker, text}]."""
    hits = list(LINE.finditer(text))
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        out.append({"local_id": m.group(1), "ts": m.group(2), "speaker": m.group(3).strip(),
                    "text": text[m.end():end].strip()})
    return out


def day_of(ts: str) -> str:
    d = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")
    return f"{d:%a %b} {d.day}"


def build(src: Path = SRC) -> tuple[list[dict], dict]:
    rows = list(csv.DictReader(src.open()))
    msgs, seen, dups, mismatch = [], set(), 0, []
    for r in rows:
        new = parse_thread(r["new_message"])
        ms = parse_thread(r["prior_context"]) + new
        trig = new[-1]["local_id"] if new else None     # trigger_message_ref is "message-NNN", not an M id
        if len(ms) != int(r["message_count"]):
            mismatch.append((r["case_id"], len(ms), r["message_count"]))
        root = None
        for m in ms:
            key = (r["conversation_ref"], m["ts"], m["speaker"], m["text"])
            if key in seen:
                dups += 1
                continue
            seen.add(key)
            mid = f"real/{r['thread_ref']}/{m['local_id']}"
            root = root or mid
            msgs.append({
                "msg_id": mid, "thread": r["thread_ref"], "turn": int(m["local_id"][1:]),
                "day": day_of(m["ts"]), "channel": "#" + r["conversation_ref"],
                "speaker": m["speaker"], "text": m["text"], "kind": "message",
                "reply_to": None, "reply_to_turn": None, "thread_ts": root, "side": False,
                "event_type": "real", "event_id": None, "fact_id": None, "item_id": None,
                "group": None, "group_fact": None, "group_value": None, "group_form": None,
                "group_origin": None, "is_agent": m["speaker"].startswith("Agent"), "ts": m["ts"],
                "trigger_of": r["case_id"] if m["local_id"] == trig else None})
    msgs.sort(key=lambda m: (m["ts"], m["msg_id"]))
    for i, m in enumerate(msgs):
        m["seq"] = i
    by_ch = Counter(m["channel"] for m in msgs)
    report = {"source": str(src), "threads": len(rows), "messages": len(msgs),
              "duplicates_dropped": dups, "count_mismatches": mismatch,
              "agent_share": round(sum(m["is_agent"] for m in msgs) / max(len(msgs), 1), 3),
              "speakers": len({m["speaker"] for m in msgs}),
              "per_channel": dict(sorted(by_ch.items())),
              "span": [msgs[0]["ts"], msgs[-1]["ts"]] if msgs else None}
    return msgs, report


def main():
    msgs, report = build()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "messages.jsonl").write_text("".join(json.dumps(m) + "\n" for m in msgs))
    (OUT / "build_report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps({k: v for k, v in report.items() if k != "per_channel"}, indent=1))
    print("per channel:", report["per_channel"])
    print(f"-> {OUT}/messages.jsonl  (git-ignored)")


if __name__ == "__main__":
    main()
