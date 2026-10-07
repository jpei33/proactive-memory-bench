"""Run the fixed judge over decision points x memory conditions.

    python -m judge.run --conditions S0,OR,E3 --n 20            # 4.1 smoke test (60 live calls)
    python -m judge.run --conditions S0,OR,A1,...  --all        # full run (4.3; Batch API comes later)

One JSONL per condition and budget: data/runs/<cond>_b<budget>.jsonl, one row per point, appended
and resumable (points already in the file are skipped). Every row keeps the exact memory text.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from judge.conditions import build, prefetch_all
from judge.prompt import system_prompt, user_prompt

LABELS = {"IGNORE", "TRACK", "INTERVENE"}
RUNS = Path("data/runs")


def parse_reply(text: str) -> dict | None:
    from sim.llm import parse_json
    try:
        j = parse_json(text)
    except ValueError:
        return None
    lab = str(j.get("label", "")).strip().upper()
    if lab not in LABELS:
        return None
    try:
        sev = int(j.get("severity", 1))
    except (TypeError, ValueError):
        sev = 1
    return {"label": lab, "severity": 1 if lab == "TRACK" else max(1, min(3, sev)),
            "cited_value": str(j.get("cited_value", "")), "reason": str(j.get("reason", ""))}


def judge_agentic(point, arm, budget, model, effort):
    from judge.conditions import ws_data
    from label.context import recent, today
    from memory.agentic import History, run_agent
    from memory.base import deliveries, window
    d, msgs, by_id, plants = ws_data(point["ws"])
    seq, ch = point["seq"], point["channel"]
    from judge.conditions import point_view
    hist = History(msgs, seq, point["ws"])
    win_ids, win_text, _, day = point_view(point)
    user = user_prompt(day, "(none pre-loaded; use your tools to search earlier messages)", ch, win_text)
    out, r, trace, tot = None, None, [], {}
    for attempt in range(3):
        hist.returned = []
        r, trace, tot = run_agent(system_prompt(), user, hist, arm, model, effort, seed=attempt)
        out = parse_reply(r.text)
        if out:
            break
    got = sorted(set(hist.returned))
    p = point if point.get("evidence_groups") else plants.get(point.get("plant_id") or "")
    if p and p.get("evidence_groups"):
        from memory.base import Chunk
        fake = [Chunk("AG", tuple(got), 0, 0, "")] if got else []
        dl = deliveries(fake, win_ids, p)["all"]
    else:
        dl = "n/a"
    return {"point_id": point["point_id"], "ws": point["ws"], "condition": arm, "budget": budget,
            "kind": point["kind"], "plant_id": point.get("plant_id"),
            **(out or {"label": "INVALID", "severity": None, "cited_value": "", "reason": r.text[:300]}),
            "retrieved": got, "delivery": dl, "memory_text": "\n".join(fmt_trace(trace)),
            "in_tok": tot["in"], "out_tok": tot["out"], "cache_read_tok": tot["cache_read"],
            "latency_s": round(tot["latency"], 2), "cached": r.cached, "tool_calls": len(trace),
            "bad_tool_calls": tot.get("bad_tool", 0), "trace": trace, "attempts": attempt + 1}


def fmt_trace(trace):
    return [f"{t['tool']}({json.dumps(t['input'])})" for t in trace]


class _R:
    def __init__(self, text):
        self.text, self.in_tok, self.out_tok, self.cache_read_tok = text, None, None, 0
        self.latency_s, self.cached = None, None


def _openai(system, user, model):
    from label.llm_label import call               # disk-cached, retries on rate limits
    return _R(call("openai", model, system, user))


def judge_one(point, cond, budget, model, effort):
    if cond.startswith("AG-"):
        if model.startswith("gpt"):
            raise SystemExit("agentic arms use Anthropic tool calling; not supported with a GPT judge")
        return judge_agentic(point, cond, budget, model, effort)
    from sim.llm import complete
    ctx = build(point, cond, budget)
    user = user_prompt(ctx["today"], ctx["memory"], ctx["channel"], ctx["window"])
    out, r = None, None
    for attempt in range(3):                       # re-sample on invalid JSON
        if model.startswith("gpt"):                # cross-family judge via OpenAI (same prompt)
            r = _openai(system_prompt(), user + ("" if attempt == 0 else f"\n(attempt {attempt + 1})"), model)
        else:
            r = complete(system_prompt(), user, model=model, max_tokens=2000, effort=effort,
                         cache_system=True, seed=attempt)
        out = parse_reply(r.text)
        if out:
            break
    row = {"point_id": point["point_id"], "ws": point["ws"], "condition": cond, "budget": budget,
           "kind": point["kind"], "plant_id": point.get("plant_id"),
           **(out or {"label": "INVALID", "severity": None, "cited_value": "", "reason": r.text[:300]}),
           "retrieved": ctx["retrieved"], "delivery": ctx["delivery"], "memory_text": ctx["memory"],
           "in_tok": r.in_tok, "out_tok": r.out_tok, "cache_read_tok": r.cache_read_tok,
           "latency_s": r.latency_s, "cached": r.cached, "tool_calls": 0, "attempts": attempt + 1}
    return row


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--conditions", required=True)
    ap.add_argument("--n", type=int, default=20, help="random sample of points (ignored with --all)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--budget", type=int, default=1500)
    ap.add_argument("--effort", default="low")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--judge-model", help="override JUDGE_MODEL; conditions get a ~tag suffix (e.g. ~haiku)")
    ap.add_argument("--tag", help="suffix for condition names (default with --judge-model: model family)")
    ap.add_argument("--points", default="data/eval_points.json", help="decision points file")
    ap.add_argument("--out-dir", default=str(RUNS), help="where run JSONLs go")
    a = ap.parse_args()
    model = a.judge_model or os.environ["JUDGE_MODEL"]
    if a.effort in ("", "none"):
        a.effort = None
    conds = a.conditions.split(",")
    tag = a.tag or (next((f for f in ("haiku", "sonnet", "opus", "gpt") if f in a.judge_model), "alt")
                    if a.judge_model else None)
    if tag:
        conds = [f"{c}~{tag}" for c in conds]
    points = json.load(open(a.points))
    out_dir = Path(a.out_dir)
    if not a.all:                                  # stratified-ish sample: keep some triggers in it
        rng = random.Random(1)
        trig = [p for p in points if p["kind"] in ("plant_trigger", "decoy_trigger")]
        rest = [p for p in points if p not in trig]
        points = rng.sample(trig, a.n // 2) + rng.sample(rest, a.n - a.n // 2)
    prefetch_all(points, [c for c in conds if not c.startswith("AG-")])
    if any(c == "AG-both" for c in conds):            # semantic_search embeds single messages
        from judge.conditions import ws_data
        from memory.base import line
        from memory.retrievers import prefetch
        prefetch(list({line(m) for p in points for m in ws_data(p["ws"])[1]}), "d")

    out_dir.mkdir(parents=True, exist_ok=True)
    gold = {g["point_id"]: g["label"] for g in json.load(open("data/gold/labels.json"))}
    gold.update({p["point_id"]: p["gold_label"] for p in points if p.get("gold_label")})
    for cond in conds:
        path = out_dir / f"{cond}_b{a.budget}.jsonl"
        old = [json.loads(l) for l in path.open()] if path.exists() else []
        if any(r["label"] == "INVALID" for r in old):       # drop invalid rows so they get redone
            old = [r for r in old if r["label"] != "INVALID"]
            path.write_text("".join(json.dumps(r) + "\n" for r in old))
        done = {r["point_id"] for r in old}
        todo = [p for p in points if p["point_id"] not in done]
        with ThreadPoolExecutor(4 if cond.startswith("AG-") else a.workers) as ex:
            rows = list(ex.map(lambda p: judge_one(p, cond, a.budget, model, a.effort), todo))
        with path.open("a") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        allrows = [json.loads(l) for l in path.open()]
        mine = [r for r in allrows if r["point_id"] in {p["point_id"] for p in points}]
        inv = sum(r["label"] == "INVALID" for r in mine)
        acc = sum(r["label"] == gold.get(r["point_id"]) for r in mine) / max(len(mine), 1)
        tok_in = sum(r["in_tok"] or 0 for r in rows) / max(len(rows), 1)
        tok_out = sum(r["out_tok"] or 0 for r in rows) / max(len(rows), 1)
        print(f"{cond:<4} {len(rows)} new rows -> {path} | invalid {inv} | agree w/ gold {acc:.0%} "
              f"| avg in {tok_in:.0f} tok, out {tok_out:.0f} tok, cache_read {sum(r['cache_read_tok'] or 0 for r in rows)}")


if __name__ == "__main__":
    main()
