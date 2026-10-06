"""Run non-agentic judge conditions through the Anthropic Message Batches API (50% price).

    python -m judge.batch submit --conditions S0,OR,Cs2,A1,...,E3 [--budget 1500]
    python -m judge.batch status
    python -m judge.batch collect          # when status says ended; appends rows to data/runs/*.jsonl

One batch per condition. Points already in data/runs/<cond>_b<budget>.jsonl are skipped, so submit is
safe to re-run. The manifest (data/runs/batches/<batch_id>.jsonl) keeps, per request, the point and the
exact memory text the judge saw; collect joins results back to it. Replies that fail to parse are left
out of the run file: rerun them live with judge.run (it fills exactly the missing points).
Request params match judge.run exactly (same model, prompt, rubric caching, effort, max_tokens).
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from judge.conditions import build, prefetch_all
from judge.prompt import system_prompt, user_prompt
from judge.run import RUNS, parse_reply

BATCH_DIR = RUNS / "batches"


def params(model, system, user, effort):
    p = {"model": model, "max_tokens": 2000,
         "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
         "messages": [{"role": "user", "content": user}]}
    if effort:
        p["output_config"] = {"effort": effort}
    return p


def submit(conds, budget, effort, limit=None, model=None, tag=None, points_file="data/eval_points.json",
           out_dir=RUNS):
    from sim.llm import client
    model = model or os.environ["JUDGE_MODEL"]
    if tag:
        conds = [f"{c}~{tag}" for c in conds]
    points = json.load(open(points_file))
    if limit:
        points = points[:limit]
    prefetch_all(points, [c for c in conds if not c.startswith("AG-")])
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    system = system_prompt()
    for cond in conds:
        if cond.startswith("AG-"):
            print(f"{cond}: agentic arms run live (python -m judge.run --conditions {cond} --all)")
            continue
        path = Path(out_dir) / f"{cond}_b{budget}.jsonl"
        done = {json.loads(l)["point_id"] for l in path.open()} if path.exists() else set()
        pending = set()                                   # already submitted, not yet collected
        for m in BATCH_DIR.glob("*.jsonl"):
            if (BATCH_DIR / f"{m.stem}.collected").exists():
                continue
            for l in m.open():
                r = json.loads(l)
                if r["condition"] == cond and r["budget"] == budget and r.get("out_dir", str(RUNS)) == str(out_dir):
                    pending.add(r["point_id"])
        todo = [p for p in points if p["point_id"] not in done | pending]
        if not todo:
            print(f"{cond}: nothing to submit ({len(done)} done, {len(pending)} pending)")
            continue
        reqs, manifest = [], []
        for i, p in enumerate(todo):
            ctx = build(p, cond, budget)
            cid = f"{'P-' if str(out_dir) != str(RUNS) else ''}{cond}-b{budget}-{i}".replace("_", "-").replace("+", "p").replace("~", "-t-").replace("@", "a")
            reqs.append({"custom_id": cid,
                         "params": params(model, system, user_prompt(ctx["today"], ctx["memory"],
                                                                     ctx["channel"], ctx["window"]), effort)})
            manifest.append({"custom_id": cid, "model": model, "out_dir": str(out_dir), "condition": cond, "budget": budget, "point_id": p["point_id"],
                             "ws": p["ws"], "kind": p["kind"], "plant_id": p.get("plant_id"),
                             "retrieved": ctx["retrieved"], "delivery": ctx["delivery"], "memory_text": ctx["memory"]})
        b = client().messages.batches.create(requests=reqs)
        with (BATCH_DIR / f"{b.id}.jsonl").open("w") as f:
            for m in manifest:
                f.write(json.dumps(m) + "\n")
        print(f"{cond}: submitted {len(reqs)} requests -> batch {b.id}")


def status():
    from sim.llm import client
    for m in sorted(BATCH_DIR.glob("*.jsonl")):
        if (BATCH_DIR / f"{m.stem}.collected").exists():
            continue
        b = client().messages.batches.retrieve(m.stem)
        c = b.request_counts
        cond = json.loads(m.open().readline())["condition"]
        print(f"{m.stem} {cond:<5} {b.processing_status:<12} ok {c.succeeded} err {c.errored} "
              f"processing {c.processing} expired {c.expired}")


def collect():
    from sim.llm import client
    tot_in = tot_out = tot_cache = 0
    spend_alt = {}
    for m in sorted(BATCH_DIR.glob("*.jsonl")):
        flag = BATCH_DIR / f"{m.stem}.collected"
        if flag.exists():
            continue
        b = client().messages.batches.retrieve(m.stem)
        if b.processing_status != "ended":
            print(f"{m.stem}: still {b.processing_status}, skipped")
            continue
        man = {r["custom_id"]: r for r in map(json.loads, m.open())}
        rows, bad = [], 0
        for res in client().messages.batches.results(m.stem):
            meta = man[res.custom_id]
            if res.result.type != "succeeded":
                bad += 1
                continue
            msg = res.result.message
            text = "".join(bl.text for bl in msg.content if bl.type == "text")
            out = parse_reply(text)
            if not out:
                bad += 1
                continue
            u = msg.usage
            cr = getattr(u, "cache_read_input_tokens", 0) or 0
            mdl = meta.get("model") or os.environ["JUDGE_MODEL"]
            if mdl == os.environ["JUDGE_MODEL"]:
                tot_in += u.input_tokens; tot_out += u.output_tokens; tot_cache += cr
            else:
                a_ = spend_alt.setdefault(mdl, [0, 0, 0]); a_[0] += u.input_tokens; a_[1] += u.output_tokens; a_[2] += cr
            rows.append({"point_id": meta["point_id"], "ws": meta["ws"], "condition": meta["condition"],
                         "budget": meta["budget"], "kind": meta["kind"], "plant_id": meta["plant_id"], **out,
                         "retrieved": meta["retrieved"], "delivery": meta["delivery"],
                         "memory_text": meta["memory_text"], "in_tok": u.input_tokens, "out_tok": u.output_tokens,
                         "cache_read_tok": cr, "latency_s": None, "cached": False, "tool_calls": 0,
                         "attempts": 1, "batch_id": m.stem})
        cond, budget = rows[0]["condition"] if rows else "?", rows[0]["budget"] if rows else 0
        first = next(iter(man.values()))
        path = Path(first.get("out_dir", str(RUNS))) / f"{cond}_b{budget}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        done = {json.loads(l)["point_id"] for l in path.open()} if path.exists() else set()
        with path.open("a") as f:
            for r in rows:
                if r["point_id"] not in done:
                    f.write(json.dumps(r) + "\n")
        flag.write_text("")
        print(f"{m.stem} {cond}: {len(rows)} rows -> {path} ({bad} failed/unparsable: rerun live with judge.run)")
    log_spend(tot_in, tot_out, tot_cache)
    for mdl, (i_, o_, c_) in spend_alt.items():
        log_spend(i_, o_, c_, mdl)


def log_spend(tin, tout, tcache, model=None):
    if not (tin or tout):
        return
    p = json.load(open("eval/prices.json"))
    model = model or os.environ["JUDGE_MODEL"]
    pr = next(v for k, v in p.items() if not k.startswith("_") and model.startswith(k))
    usd = (tin * pr["batch_in"] + tout * pr["batch_out"] + tcache * pr["cache_read"] * 0.5) / 1e6
    log = Path("results/cost_log.md")
    if not log.exists():
        log.write_text("# Cost log\n\n| what | in tok | out tok | cache read | $ |\n|---|---|---|---|---|\n")
    with log.open("a") as f:
        f.write(f"| judge batch collect ({model}) | {tin:,} | {tout:,} | {tcache:,} | {usd:.2f} |\n")
    print(f"batch spend this collect: ${usd:.2f} (logged to {log})")


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["submit", "status", "collect"])
    ap.add_argument("--conditions", default="")
    ap.add_argument("--budget", type=int, default=1500)
    ap.add_argument("--effort", default="low")
    ap.add_argument("--limit", type=int, help="only the first N points (testing)")
    ap.add_argument("--judge-model", help="override JUDGE_MODEL (robustness); conditions get ~tag")
    ap.add_argument("--tag", help="suffix for condition names, e.g. s1 for a repeat run (noise floor)")
    ap.add_argument("--points", default="data/eval_points.json")
    ap.add_argument("--out-dir", default=str(RUNS))
    a = ap.parse_args()
    if a.effort in ("", "none"):
        a.effort = None
    if a.cmd == "submit":
        tag = a.tag
        if a.judge_model and not tag:
            tag = next((f for f in ("haiku", "sonnet", "opus", "gpt") if f in a.judge_model), "alt")
        submit(a.conditions.split(","), a.budget, a.effort, a.limit, a.judge_model, tag, a.points, a.out_dir)
    elif a.cmd == "status":
        status()
    else:
        collect()


if __name__ == "__main__":
    main()
