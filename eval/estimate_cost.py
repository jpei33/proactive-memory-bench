"""Estimate the API cost of the rest of the experiment, and report what's been spent so far.

    python -m eval.estimate_cost                 # token sizes from text length (chars / 4)
    python -m eval.estimate_cost --calibrate     # measure the chars-per-token ratio with the API's
                                                 # token-counting endpoint first (needs your API key)

Prompt sizes are built from the real corpus: the rubric, actual 15-message channel windows at the
decision points, the retrieval budget, real message lengths. Each call type is priced with the
model it will use (from .env) and eval/prices.json. Estimates are conservative: no prompt-cache
discounts are assumed, so caching the rubric only makes the real bill smaller.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")
ALL = ["ando", "anthropic", "openai", "xai"]
BUDGET = 1500          # retrieved-memory tokens handed to the judge
CAP = 100.0            # dollars
GRID = 15              # 5 chunkers x 3 retrievers
EXTRA_BATCH = ["Cstar", "S0", "OR", "best@500", "best@4000"]
AGENTIC = ["AG-grep", "AG-both"]


def price_of(model: str, prices: dict) -> dict:
    for k, v in prices.items():
        if not k.startswith("_") and model.startswith(k):
            return v
    raise KeyError(f"no price for {model}; add it to eval/prices.json")


def spent_so_far(prices) -> dict:
    """Sum every real (non-cached) call recorded in data/cache/llm."""
    tot = defaultdict(lambda: Counter())
    for f in Path("data/cache/llm").rglob("*.json"):
        r = json.loads(f.read_text())
        t = tot[r.get("model", "?")]
        t["calls"] += 1
        t["in"] += r.get("in_tok", 0)
        t["out"] += r.get("out_tok", 0)
    out = {}
    for m, t in tot.items():
        p = price_of(m, prices)
        out[m] = (t["calls"], t["in"], t["out"], (t["in"] * p["in"] + t["out"] * p["out"]) / 1e6)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    a = ap.parse_args()
    prices = {k: v for k, v in json.load(open("eval/prices.json")).items()}
    judge = os.environ.get("JUDGE_MODEL", "claude-sonnet-5-5")
    cheap = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5")
    writer = cheap                        # Haiku-class model for rewrite / linker / segmenter / triggers
    labeler = "claude-opus-5-5"           # deliberately a different model from the judge

    # ---------------------------------------------------------------- measure the corpus
    from label.context import load_ws, recent, team_facts
    rubric = Path("rubric.md").read_text()
    points = json.load(open("data/eval_points.json"))
    ws_data = {ws: load_ws(ws) for ws in ALL}
    win_chars, facts_chars, msg_chars = [], [], []
    n_msgs = n_link = n_seg = 0
    for ws, (d, msgs, _) in ws_data.items():
        n_msgs += len(msgs)
        struct = {t["id"]: t.get("structure", "flat") for t in d["threads"]}
        n_link += sum(1 for m in msgs if struct[m["thread"]] != "threaded" and m["kind"] != "reaction"
                      and not (m.get("group") and m.get("reply_to")))
        n_seg += sum(math.ceil(c / 20) for c in Counter(m["channel"] for m in msgs).values())
        msg_chars += [len(m["text"]) + 30 for m in msgs]
    for p in points:
        d, msgs, _ = ws_data[p["ws"]]
        win_chars.append(len(recent(msgs, p["seq"], p["channel"])))
        facts_chars.append(len(team_facts(d, msgs, p["seq"])))
    avg = lambda xs: sum(xs) / len(xs)

    cpt = 4.0                              # characters per token
    if a.calibrate:
        import anthropic
        c = anthropic.Anthropic()
        sample = rubric + "\n" + "\n".join(recent(*ws_data["ando"][1:2], p["seq"], p["channel"])
                                           for p in points[:5] if p["ws"] == "ando")
        n = c.messages.count_tokens(model=judge, messages=[{"role": "user", "content": sample}]).input_tokens
        cpt = len(sample) / n
        print(f"calibrated: {cpt:.2f} characters per token (from {n} tokens)\n")
    tok = lambda chars: chars / cpt

    rubric_t, win_t, facts_t, msg_t = tok(len(rubric) + 400), tok(avg(win_chars)), tok(avg(facts_chars)), tok(avg(msg_chars))
    P = len(points)
    plants_iv = sum(1 for p in points if p["kind"] == "plant_trigger" and p["gold_label"] == "INTERVENE")

    # ---------------------------------------------------------------- call types
    # (name, model, calls, input tokens per call, output tokens per call, batched?)
    rows = [
        ("judge: 15 grid cells", judge, GRID * P, rubric_t + BUDGET + win_t + 60, 80, True),
        ("judge: Cstar, S0, OR, 2 budgets", judge, len(EXTRA_BATCH) * P, rubric_t + 0.7 * BUDGET + win_t + 60, 80, True),
        ("judge: AG-grep, AG-both (~2.5 calls/pt)", judge, len(AGENTIC) * P * 2.5,
         rubric_t + win_t + 300 + 1.25 * 500, 120, False),
        ("probe reader (L1b)", judge, plants_iv * (GRID + len(EXTRA_BATCH) + len(AGENTIC)), BUDGET + win_t + 120, 30, True),
        ("E rewrite (1 per message)", writer, n_msgs, 250 + 10 * msg_t + msg_t, 60, True),
        ("C linker (unthreaded msgs)", writer, n_link, 80 + 13 * msg_t, 5, True),
        ("D segmenter (per 20 msgs/channel)", writer, n_seg, 60 + 40 * msg_t, 40, True),
        ("probe triggers (~110)", writer, 110, 150 + 5 * msg_t, 40, True),
        ("LLM labeler: calibrate + label", labeler, 3 * 30 + 70 + 100, rubric_t + facts_t + win_t + 80, 80, True),
        ("robustness: 2nd judge, 8 conditions", cheap, 8 * P, rubric_t + BUDGET + win_t + 60, 80, True),
    ]
    optional = [("optional: every-message check, 3 conditions", judge, 3 * n_msgs, rubric_t + BUDGET + win_t + 60, 80, True)]

    def cost(model, calls, i, o, batch):
        p = price_of(model, prices)
        pi, po = (p["batch_in"], p["batch_out"]) if batch else (p["in"], p["out"])
        return calls * (i * pi + o * po) / 1e6

    print(f"corpus: {n_msgs} messages, {P} decision points, {plants_iv} INTERVENE plants; "
          f"avg window {win_t:.0f} tok, rubric+instructions {rubric_t:.0f} tok, budget {BUDGET} tok\n")
    print(f"{'call type':<44} {'model':<26} {'calls':>7} {'in tok':>9} {'out tok':>8} {'batch':>5} {'$':>8}")
    total = 0.0
    for name, model, calls, i, o, batch in rows + optional:
        c = cost(model, calls, i, o, batch)
        if not name.startswith("optional"):
            total += c
        print(f"{name:<44} {model:<26} {calls:>7.0f} {calls * i / 1e6:>8.2f}M {calls * o / 1e6:>7.2f}M "
              f"{'yes' if batch else 'no':>5} {c:>8.2f}")
    print(f"\n{'ESTIMATED REMAINING (excl. optional)':<44} {'':<26} {'':>7} {'':>9} {'':>8} {'':>5} {total:>8.2f}")

    spent = spent_so_far(prices)
    s = sum(v[3] for v in spent.values())
    print(f"\nspent so far (from data/cache/llm, list prices):")
    for m, (calls, i, o, c) in spent.items():
        print(f"  {m:<26} {calls:>6} calls  {i / 1e6:>6.2f}M in  {o / 1e6:>5.2f}M out  ${c:>7.2f}")
    print(f"  {'TOTAL':<26} {'':>6}        {'':>6}      {'':>5}       ${s:>7.2f}")
    left = CAP - s
    print(f"\ncap ${CAP:.0f}: spent ${s:.2f}, estimated remaining ${total:.2f} -> "
          f"{'fits' if total <= left else 'OVER'} (headroom ${left - total:.2f})")
    if total > left:
        print("cut order: (1) judge ordinary points for only 6 conditions; (2) drop the hybrid column from judge runs")


if __name__ == "__main__":
    main()
