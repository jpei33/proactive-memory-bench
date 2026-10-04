"""Pick the decision points every memory condition is evaluated on.

    python -m eval.select_points            # writes data/eval_points.json, logs counts

A decision point is "the moment right after message X": the judge sees the window ending
at X and decides IGNORE / TRACK / INTERVENE. Every memory condition still *writes* every
message in order; the judge only *reads* at these points.

Kinds
  plant_trigger   every plant's trigger message (gold label from the ledger)
  decoy_trigger   every decoy's trigger message (gold label IGNORE)
  plant_after     the next 2 messages in the same channel after each INTERVENE plant
                  trigger, so a late-but-acceptable intervention (within k=2) can be scored
  ordinary        random other messages (~38 per workspace, 150 total), to measure false
                  interventions in normal chat; their labels come from humans / the labeler
Ordinary points avoid anything within 3 messages (same channel) of a trigger, and reactions.
"""
from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path

ALL = ["ando", "anthropic", "openai", "xai"]
K_AFTER = 2      # timing tolerance for INTERVENE plants
GUARD = 3        # ordinary points stay this many channel messages away from any trigger


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", default=",".join(ALL))
    ap.add_argument("--ordinary", type=int, default=150)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="data/eval_points.json")
    a = ap.parse_args()
    names = a.ws.split(",")
    rng = random.Random(a.seed)
    quota = {ws: a.ordinary // len(names) + (i < a.ordinary % len(names)) for i, ws in enumerate(names)}

    points = []
    for ws in names:
        base = Path(f"data/workspaces/{ws}")
        msgs = [json.loads(l) for l in (base / "messages.jsonl").read_text().splitlines()]
        plants = [json.loads(l) for l in (base / "plants.jsonl").read_text().splitlines()]
        by_id = {m["msg_id"]: m for m in msgs}
        chan_pos, chan_seq = {}, {}                      # position of each message within its channel
        for m in msgs:
            lst = chan_seq.setdefault(m["channel"], [])
            chan_pos[m["msg_id"]] = len(lst)
            lst.append(m["msg_id"])

        chosen: dict[str, dict] = {}

        def add(mid, kind, **extra):
            if mid in chosen:                            # a trigger wins over a follow-up
                return
            m = by_id[mid]
            chosen[mid] = {"point_id": mid, "ws": ws, "seq": m["seq"], "channel": m["channel"],
                           "thread": m["thread"], "kind": kind, **extra}

        # 1. triggers
        for p in plants:
            add(p["trigger_msg"], f"{p['kind']}_trigger", plant_id=p["plant_id"],
                gold_label=p["gold_label"], severity=p["severity"])
        # 2. follow-ups after INTERVENE plants
        for p in plants:
            if p["kind"] == "plant" and p["gold_label"] == "INTERVENE":
                ch = by_id[p["trigger_msg"]]["channel"]
                i = chan_pos[p["trigger_msg"]]
                for off, mid in enumerate(chan_seq[ch][i + 1: i + 1 + K_AFTER], start=1):
                    add(mid, "plant_after", plant_id=p["plant_id"], offset=off, gold_label=None)
        # 3. ordinary messages, away from triggers
        near = set()
        for p in plants:
            ch = by_id[p["trigger_msg"]]["channel"]
            i = chan_pos[p["trigger_msg"]]
            near.update(chan_seq[ch][max(0, i - GUARD): i + GUARD + 1])
        pool = [m["msg_id"] for m in msgs
                if m["msg_id"] not in chosen and m["msg_id"] not in near and m["kind"] != "reaction"]
        for mid in sorted(rng.sample(pool, min(quota[ws], len(pool))), key=lambda x: by_id[x]["seq"]):
            add(mid, "ordinary", plant_id=None, gold_label=None)

        points += sorted(chosen.values(), key=lambda x: x["seq"])

    Path(a.out).write_text(json.dumps(points, indent=1))

    # summary, also appended to results/corpus_stats.txt
    kinds = ["plant_trigger", "decoy_trigger", "plant_after", "ordinary"]
    lines = ["Decision points (eval/select_points.py)", "---------------------------------------",
             f"{'workspace':<10}  " + "  ".join(f"{k:>13}" for k in kinds) + f"  {'total':>5}"]
    for ws in names:
        c = Counter(p["kind"] for p in points if p["ws"] == ws)
        lines.append(f"{ws:<10}  " + "  ".join(f"{c[k]:>13}" for k in kinds) + f"  {sum(c.values()):>5}")
    c = Counter(p["kind"] for p in points)
    lines.append(f"{'TOTAL':<10}  " + "  ".join(f"{c[k]:>13}" for k in kinds) + f"  {len(points):>5}")
    lines.append(f"side messages among ordinary points: "
                 f"{sum(1 for p in points if p['kind'] == 'ordinary' and '/s' in p['point_id'])}")
    summary = "\n".join(lines)
    print(summary)
    print(f"-> {a.out}")

    stats = Path("results/corpus_stats.txt")
    if stats.exists():
        txt = re.sub(r"\n*Decision points \(eval/select_points\.py\).*", "", stats.read_text(), flags=re.S)
        stats.write_text(txt.rstrip() + "\n\n" + summary + "\n")


if __name__ == "__main__":
    main()
