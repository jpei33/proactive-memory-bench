"""Find messages that restate a plant's answer in a form our regex checks can't see
("AND-341 is mine now" said by Oli = owner is Oli).

    python -m world.restatement_audit --all            # writes data/workspaces/<ws>/restatements.json
    python -m world.restatement_audit --all --show     # print the hits

For each fact plant: every message after the origin evidence and before the trigger (all channels,
excluding the evidence itself) is shown, numbered, to the model with the plant's probe question
and its answer. The model returns the messages from which a reader could get that answer.
memory.base.load_plants() merges the hits as extra evidence groups (form "restatement",
origin False) and sets restated=True, so delivery counts them. plants.jsonl is not modified, so
sim.rebuild_plants can't wipe the audit.
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

AUDIT = """You are auditing a team chat log for a memory benchmark.

Question: {PROBE}
Correct answer at this point: {ANSWER}

Below are chat messages, oldest first. Find every message from which a reader who sees ONLY that
one message (with its speaker, date and channel) could learn the correct answer. Count implicit
statements: "it's mine now" said by the owner, "still haven't sent it" for an unfinished task,
a quoted figure equal to the answer. Do NOT count messages that merely mention the topic, ask
about it, or state a different (old or wrong) value.

{NUMBERED}

Return JSON only: {"hits": [{"n": <message number>, "why": "<short reason>"}]}  (empty list if none)"""

WSS = ["ando", "anthropic", "openai", "xai"]


def audit_ws(ws: str, workers: int = 8):
    from sim.llm import complete, parse_json
    base = Path(f"data/workspaces/{ws}")
    msgs = [json.loads(l) for l in (base / "messages.jsonl").read_text().splitlines()]
    raw = [json.loads(l) for l in (base / "plants.jsonl").read_text().splitlines()]
    by_id = {m["msg_id"]: m for m in msgs}
    # deadline_passed is skipped: "not done" is shown by absence after the check point, so there is
    # nothing to restate (the first audit's hits there were all false positives).
    plants = [p for p in raw if p.get("kind") == "plant" and p.get("evidence_groups") and p.get("probe")
              and p["type"] != "deadline_passed"]

    def one(p):
        ev = {i for g in p["evidence_groups"] for i in g["msgs"]}
        origin = [i for g in p["evidence_groups"] if g.get("origin") for i in g["msgs"]] or list(ev)
        lo, hi = max(by_id[i]["seq"] for i in origin), by_id[p["trigger_msg"]]["seq"]
        cands = [m for m in msgs if lo < m["seq"] < hi and m["msg_id"] not in ev and m["kind"] == "message"]
        if not cands:
            return p["plant_id"], [], 0
        numbered = "\n".join(f"[{k}] ({m['day']} {m['channel']}) {m['speaker']}: {m['text']}"
                             for k, m in enumerate(cands))
        prompt = (AUDIT.replace("{PROBE}", p["probe"]).replace("{ANSWER}", str(p["gold_value"]))
                  .replace("{NUMBERED}", numbered))
        r = complete(None, prompt, max_tokens=3000)          # SIM_MODEL (Sonnet): precision matters here
        try:
            hits = parse_json(r.text).get("hits", [])
        except (ValueError, AttributeError):
            hits = []
        out = []
        for h in hits:
            try:
                k = int(h["n"])
            except (KeyError, TypeError, ValueError):
                continue
            if 0 <= k < len(cands):
                m = cands[k]
                out.append({"msg_id": m["msg_id"], "speaker": m["speaker"], "text": m["text"],
                            "why": h.get("why", ""), "event_type": m.get("event_type")})
        return p["plant_id"], out, len(cands)

    with ThreadPoolExecutor(workers) as ex:
        res = list(ex.map(one, plants))
    old = {}
    if (base / "restatements.json").exists():           # keep human verdicts across reruns
        for pid, hs in json.loads((base / "restatements.json").read_text()).items():
            for h in hs:
                if "verdict" in h:
                    old[(pid, h["msg_id"])] = (h["verdict"], h.get("review", ""))
    for pid, hits, _ in res:
        for h in hits:
            if (pid, h["msg_id"]) in old:
                h["verdict"], h["review"] = old[(pid, h["msg_id"])]
    audit = {pid: hits for pid, hits, _ in res}
    (base / "restatements.json").write_text(json.dumps(audit, indent=1))
    return res


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--show", action="store_true", help="print existing results, no API calls")
    a = ap.parse_args()
    for ws in (WSS if a.all else [a.ws]):
        if a.show:
            audit = json.loads(Path(f"data/workspaces/{ws}/restatements.json").read_text())
            res = [(pid, hits, None) for pid, hits in audit.items()]
        else:
            res = audit_ws(ws)
        hit = [r for r in res if r[1]]
        print(f"{ws}: {len(res)} fact plants audited, {len(hit)} have hidden restatements "
              f"({sum(len(r[1]) for r in res)} messages)")
        for pid, hits, n in hit:
            for h in hits:
                print(f"  {h.get('verdict', 'unreviewed'):<10} {pid:<14} {h['msg_id']:<18} [{h['event_type']}] {h['speaker']}: {h['text'][:70]}"
                      f"\n{'':28}why: {h['why'][:100]}")


if __name__ == "__main__":
    main()
