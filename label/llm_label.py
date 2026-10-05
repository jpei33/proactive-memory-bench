"""LLM labeler: labels a sheet exactly as a human would (same rubric, same row rendering).

    python -m label.llm_label --sheet overlap                    # all 100 rows
    python -m label.llm_label --sheet overlap --split dev        # only the 30 dev rows (prompt tuning)
    python -m label.llm_label --sheet overlap --prompt v2        # after editing PROMPTS below

Provider/model come from .env:
    LABELER_PROVIDER=openai          (or anthropic)
    LABELER_MODEL=<model id>         e.g. your strongest available GPT model
    OPENAI_API_KEY=...
Writes label/sheet_<sheet>_<model>_<prompt>.csv (row,label,severity,notes). Every API response is
cached under data/cache/labeler/, so reruns are free and reproducible.

The dev/test split of the overlap sheet (30 / 70 rows, fixed seed) lives in split_rows(); tune
the prompt on dev only, then run test exactly once.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import re
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")
CACHE = Path("data/cache/labeler")

PROMPTS = {
    "v1": """You are labeling a benchmark for AI teammates in company chat. For one decision point,
decide what an AI teammate with PERFECT MEMORY of the workspace should do right after the marked
decision message. Follow this rubric exactly:

{RUBRIC}

You are given: today's date, the team facts as of now (current values, with earlier values where a
fact changed, and open items with their check points), the channel's recent messages, and the
decision message. Work through it in this order:
1. Note every date, number, name, owner, ticket, price or promise in the decision message.
2. Look each up in the team facts: different from the current value = contradiction; matches a
   "previously" value = stale; asks about something already in the facts = repeat question.
3. Compare open items' check points with today's date.
4. Check the recent messages: already corrected or answered? self-correction? proposal? addressed to
   a specific person? personal or sensitive? -> IGNORE (tie-breaks).
5. Nothing triggered -> IGNORE, unless the message opens a new item with all three parts
   (something specific, a named owner, a check point) -> TRACK.

Reply with ONLY a JSON object:
{"label": "IGNORE" | "TRACK" | "INTERVENE", "severity": 1 | 2 | 3, "note": "<one short sentence: the fact acted on, or why not>"}""",
    "v2": """You are labeling a benchmark for AI teammates in company chat. For one decision point,
decide what an AI teammate with PERFECT MEMORY of the workspace should do right after the marked
decision message. Follow this rubric exactly:

{RUBRIC}

You are given: today's date, the team facts as of now (current values, with earlier values where a
fact changed, and open items with their check points), the channel's recent messages, and the
decision message.

KEY RULE: you judge the DECISION MESSAGE ONLY, not the conversation. Most decision points are
IGNORE. A problem that sits elsewhere in the recent messages is not a reason to intervene now.

Work through it in this order:
1. Note every date, number, name, owner, ticket, price or promise IN THE DECISION MESSAGE itself.
2. Look each up in the team facts: different from the current value = contradiction; matches a
   "previously" value = stale; asks about something already in the facts = repeat question.
   A statement that agrees with the facts ("X is still open" when it is open) is IGNORE.
3. Overdue open items: INTERVENE only if the decision message is the FIRST message after the check
   point passed (tie-break 7). If earlier recent messages were already after the check point, the
   moment has passed: IGNORE.
4. Check the recent messages: was this already corrected, questioned or answered by someone? Is it a
   self-correction, a proposal, addressed to a specific person, personal or sensitive? -> IGNORE.
5. TRACK only if the decision message opens a new item with ALL THREE parts stated explicitly: a
   specific deliverable or decision, a named owner, AND a check point (a date or an event). A
   promise with no stated check point ("I'll pull a snippet", "will post what I find") is IGNORE.
   A question asking for a decision is not TRACK.
6. Nothing triggered -> IGNORE.

Reply with ONLY a JSON object:
{"label": "IGNORE" | "TRACK" | "INTERVENE", "severity": 1 | 2 | 3, "note": "<one short sentence: the fact acted on, or why not>"}""",
}


def split_rows(n: int = 100, n_dev: int = 30, seed: int = 11) -> dict[str, set[int]]:
    rows = list(range(1, n + 1))
    random.Random(seed).shuffle(rows)
    return {"dev": set(rows[:n_dev]), "test": set(rows[n_dev:]), "all": set(rows)}


def rows_from_sheet(sheet: str) -> dict[int, str]:
    """Row number -> the exact text a human labeler saw for that row."""
    md = Path(f"label/sheet_{sheet}.md").read_text()
    parts = re.split(r"\n## Row (\d+)\n", md)
    return {int(parts[i]): parts[i + 1].strip().rstrip("-").strip() for i in range(1, len(parts), 2)}


def call(provider: str, model: str, system: str, user: str) -> str:
    key = hashlib.sha256(json.dumps([provider, model, system, user]).encode()).hexdigest()
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())["text"]
    tries = 10
    for attempt in range(tries):
        try:
            if provider == "openai":
                from openai import OpenAI
                r = OpenAI().chat.completions.create(
                    model=model, response_format={"type": "json_object"},
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
                text, usage = r.choices[0].message.content, r.usage.model_dump() if r.usage else {}
            elif provider == "anthropic":
                import anthropic
                r = anthropic.Anthropic().messages.create(model=model, max_tokens=400, system=system,
                                                          messages=[{"role": "user", "content": user}])
                text, usage = "".join(b.text for b in r.content if b.type == "text"), r.usage.model_dump()
            else:
                raise ValueError(f"unknown provider {provider}")
            break
        except Exception as e:                       # rate limits / transient errors: back off
            if attempt == tries - 1:
                raise
            if "per day" in str(e) or "insufficient_quota" in str(e):
                raise SystemExit(f"daily limit or quota hit, retrying won't help:\n{str(e)[:300]}")
            rate = "RateLimit" in type(e).__name__ or "429" in str(e)
            wait = min(20 * (attempt + 1), 90) if rate else 2 ** attempt
            print(f"  retry {attempt + 1}: {type(e).__name__} (waiting {wait}s): {str(e)[:400] if attempt == 0 else str(e)[:60]}")
            time.sleep(wait)
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"provider": provider, "model": model, "text": text, "usage": usage}))
    return text


def parse(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    out = json.loads(m.group(0)) if m else {}
    lab = str(out.get("label", "")).upper().strip()
    if lab not in ("IGNORE", "TRACK", "INTERVENE"):
        raise ValueError(f"bad label in {text[:120]!r}")
    sev = int(out.get("severity", 1)) if str(out.get("severity", "1")).strip().isdigit() else 1
    return {"label": lab, "severity": 1 if lab == "TRACK" else min(3, max(1, sev)),
            "note": str(out.get("note", ""))[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", default="overlap")
    ap.add_argument("--split", default="all", choices=["all", "dev", "test"])
    ap.add_argument("--prompt", default="v1")
    ap.add_argument("--provider", default=os.environ.get("LABELER_PROVIDER", "openai"))
    ap.add_argument("--model", default=os.environ.get("LABELER_MODEL"))
    a = ap.parse_args()
    if not a.model:
        raise SystemExit("set LABELER_MODEL in .env (and OPENAI_API_KEY for openai)")
    system = PROMPTS[a.prompt].replace("{RUBRIC}", Path("rubric.md").read_text())
    rows = rows_from_sheet(a.sheet)
    want = split_rows(len(rows))[a.split] if a.sheet == "overlap" else set(rows)
    out_path = Path(f"label/sheet_{a.sheet}_{a.model.replace('/', '-')}_{a.prompt}.csv")
    done = {}
    if out_path.exists():                            # keep rows from earlier splits
        done = {int(r["row"]): r for r in csv.DictReader(open(out_path))}
    stopped = None
    for row in sorted(want):
        try:
            res = parse(call(a.provider, a.model, system, rows[row]))
        except SystemExit as e:                      # daily cap: save what we have, rerun later
            stopped = e
            break
        done[row] = {"row": row, "label": res["label"], "severity": res["severity"], "notes": res["note"]}
        print(f"row {row:>3}: {res['label']:<9} {res['severity']}  {res['note'][:80]}")
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row", "label", "severity", "notes"])
        w.writeheader()
        for row in sorted(done):
            w.writerow(done[row])
    print(f"-> {out_path} ({len(done)} rows)")
    if stopped:
        left = len([r for r in want if r not in done])
        raise SystemExit(f"{stopped}\n\nstopped with {left} rows left; rerun the same command later (finished rows are cached)")


if __name__ == "__main__":
    main()
