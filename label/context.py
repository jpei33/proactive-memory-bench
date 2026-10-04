"""What a labeler sees for one decision point: team facts as of that moment + recent messages.

The facts box is the "perfect memory" view: every fact's value in force before the point,
plus open items (opened earlier, not yet resolved). Same template for every row, so it
doesn't reveal which rows are plants.
"""
from __future__ import annotations

import json
from pathlib import Path

from sim.run_workspace import load


def load_ws(ws: str):
    d = load(ws)
    base = Path(f"data/workspaces/{ws}")
    msgs = [json.loads(l) for l in (base / "messages.jsonl").read_text().splitlines()]
    plants = [json.loads(l) for l in (base / "plants.jsonl").read_text().splitlines()]
    return d, msgs, plants


def _seq(by_id, ws, thread, turn):
    m = by_id.get(f"{ws}/{thread}/{turn:03d}")
    return m["seq"] if m else None


def team_facts(d, msgs, q_seq: int) -> str:
    """Bullet list of fact values and open items in force just before message q_seq."""
    ws, by_id = d["workspace"], {m["msg_id"]: m for m in msgs}
    lines = []
    for f in d["facts"]:
        past = []                                   # values in force before q_seq, oldest first
        for h in f["history"]:
            s = _seq(by_id, ws, h["set_in"], h["turn"])
            if s is not None and s < q_seq:
                past.append((h["value"], by_id[f"{ws}/{h['set_in']}/{h['turn']:03d}"]["day"]))
        if past:
            cur, day = past[-1]
            line = f"- {f['entity']} ({f['attribute']}): {cur}"
            if len(past) > 1:                       # a perfect-memory teammate knows the old value too
                line += f" (changed {day}; previously {past[-2][0]})"
            lines.append(line)
    for it in d.get("open_items", []):
        o = it["opened_in"]
        so = _seq(by_id, ws, o["thread"], o["turn"])
        if so is None or so >= q_seq:
            continue
        r = it.get("resolved")
        sr = _seq(by_id, ws, r["thread"], r["turn"]) if r else None
        if sr is not None and sr < q_seq:
            continue
        who = d["_persona"][it["owner"]]["name"]
        lines.append(f"- open item: {who} to {it['what']} (check point: {it['check_point']})")
    return "\n".join(lines) or "- (nothing decided yet)"


def recent(msgs, q_seq: int, channel: str, n: int = 15) -> str:
    """The last n messages of the channel up to and including q_seq, oldest first."""
    by_id = {m["msg_id"]: m for m in msgs}
    win = [m for m in msgs if m["channel"] == channel and m["seq"] <= q_seq][-n:]
    out, day = [], None
    for m in win:
        if m["day"] != day:
            out.append(f"--- {m['day']} · {m['channel']} ---")
            day = m["day"]
        if m["kind"] == "reaction":
            tgt = by_id.get(m["reply_to"], {}).get("speaker", "?")
            out.append(f"({m['speaker']} reacted {m['text']} to {tgt}'s message)")
        else:
            out.append(f"{m['speaker']}: {m['text']}")
    return "\n".join(out)
