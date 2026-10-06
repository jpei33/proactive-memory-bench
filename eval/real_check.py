"""Real-data check on 50 decision points from real team-chat threads (private; data/real/ is git-ignored).

    python -m eval.real_check label      # GPT labeler labels all 50 rows; agreement with the Claude first pass
    python -m eval.real_check judge      # our fixed judge (same prompt + rubric) on every row, several conditions
    python -m eval.real_check review     # writes data/real/review_sheet.md + review_justin.csv for your human pass
    python -m eval.real_check report     # -> results/real_check.md (aggregate numbers only; safe to commit)

Input: data/real/candidates_claude_labeled.csv (case_id, prior_context, new_message, should_intervene, ...).
Conditions for the judge (window = what the judge sees; there is no retrieval: each case is one thread):
  FULL     whole thread before the new message            (Sonnet, the main judge)
  LAST15   only the last 15 messages before the new one    (Sonnet; tests whether older context matters)
  FULL~haiku / FULL~gpt   same as FULL with a different judge model
All per-case outputs stay in data/real/. Only aggregate numbers and case ids go to results/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

D = Path("data/real")
SRC = D / "candidates_claude_labeled.csv"
MSG = re.compile(r"(?m)^(?=M\d+ \| )")

LABEL_SYS = """You label decision points from a real team chat where people and AI agents work together.
For each case you see the earlier messages of one thread and a new message.

Question: given the prior context and the new message, should an AI teammate proactively intervene
because the new message conflicts with, invalidates, or materially changes something said earlier?

Answer yes only if a short, specific note from a teammate would clearly help right now. Answer no for
ordinary discussion, banter, questions that are simply answered, new topics, and disagreements the people
in the thread are already handling.

Return JSON only: {"should_intervene": true | false, "confidence": "low" | "medium" | "high",
"conflict": "<one sentence: what conflicts with what, or empty>"}"""


def load():
    df = pd.read_csv(SRC)
    df["claude"] = df.should_intervene.astype(int)
    return df


def msgs(prior: str) -> list[str]:
    return [m.strip() for m in MSG.split(prior) if m.strip()]


def fmt_msg(m: str) -> str:
    """'M07 | 2026-08-26T19:20:00Z | Person 1: hi' -> '[Aug 26 19:20] Person 1: hi'"""
    p = m.split(" | ", 2)
    if len(p) < 3:
        return m
    ts = p[1]
    try:
        ts = pd.Timestamp(ts).strftime("%b %d %H:%M")
    except Exception:
        pass
    return f"[{ts}] {p[2]}"


def day_of(new_message: str) -> str:
    try:
        return pd.Timestamp(new_message.split(" | ")[1]).strftime("%a %b %d")
    except Exception:
        return "unknown"


# ---------------------------------------------------------------- label
def cmd_label():
    from dotenv import load_dotenv
    load_dotenv(".env")
    from label.llm_label import call
    from sim.llm import parse_json
    model = os.environ["LABELER_MODEL"]
    df = load()

    def one(r):
        user = f"PRIOR MESSAGES:\n{r.prior_context}\n\nNEW MESSAGE:\n{r.new_message}"
        try:
            j = parse_json(call("openai", model, LABEL_SYS, user))
            return {"case_id": r.case_id, "gpt": int(bool(j.get("should_intervene"))),
                    "gpt_conf": j.get("confidence", ""), "gpt_conflict": j.get("conflict", "")}
        except Exception as e:
            return {"case_id": r.case_id, "gpt": None, "gpt_conf": "", "gpt_conflict": f"ERROR {e}"}

    with ThreadPoolExecutor(4) as ex:
        out = pd.DataFrame(list(ex.map(one, df.itertuples())))
    out.to_csv(D / f"labels_gpt_{model}.csv", index=False)
    agree(df.merge(out, on="case_id"), "claude", "gpt")


def agree(m, a, b):
    from sklearn.metrics import cohen_kappa_score, confusion_matrix
    m = m.dropna(subset=[a, b])
    x, y = m[a].astype(int), m[b].astype(int)
    print(f"{a} vs {b}: n={len(m)}, raw agreement {(x == y).mean():.2f}, kappa {cohen_kappa_score(x, y):.3f}")
    print(f"  confusion (rows {a} 0/1, cols {b} 0/1): {confusion_matrix(x, y, labels=[0, 1]).tolist()}")
    for r in m[x != y].itertuples():
        print(f"  disagree {r.case_id}: {a}={getattr(r, a)} {b}={getattr(r, b)}")


# ---------------------------------------------------------------- judge
CONDS = {"FULL": None, "LAST15": 15, "FULL~haiku": None, "FULL~gpt": None}


def judge_one(row, cond):
    from judge.prompt import system_prompt, user_prompt
    from judge.run import parse_reply
    ms = msgs(row.prior_context)
    n = CONDS[cond]
    shown = ms[-n:] if n else ms
    window = "\n".join(fmt_msg(m) for m in shown + [row.new_message.strip()])
    note = "(none: this is one thread; its earlier messages are shown below)" if not n else \
        "(none; only the most recent messages are shown below)"
    user = user_prompt(day_of(row.new_message), note, "this thread", window)
    sysm = system_prompt()
    if cond.endswith("~gpt"):
        from label.llm_label import call
        text = call("openai", os.environ["LABELER_MODEL"], sysm, user)
        tin = tout = None
    else:
        from sim.llm import complete
        model = os.environ["CHEAP_JUDGE_MODEL"] if cond.endswith("~haiku") else os.environ["JUDGE_MODEL"]
        r = complete(sysm, user, model=model, max_tokens=2000,
                     effort=None if cond.endswith("~haiku") else "low", cache_system=True)
        text, tin, tout = r.text, r.in_tok, r.out_tok
    out = parse_reply(text) or {"label": "INVALID", "severity": None, "cited_value": "", "reason": text[:300]}
    return {"case_id": row.case_id, "condition": cond, **out, "n_msgs_shown": len(shown) + 1,
            "in_tok": tin, "out_tok": tout}


def cmd_judge(conds):
    from dotenv import load_dotenv
    load_dotenv(".env")
    df = load()
    path = D / "judge_runs.jsonl"
    done = set()
    if path.exists():
        done = {(json.loads(l)["case_id"], json.loads(l)["condition"]) for l in path.open()
                if json.loads(l)["label"] != "INVALID"}
    jobs = [(r, c) for c in conds for r in df.itertuples() if (r.case_id, c) not in done]
    with ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(lambda rc: judge_one(*rc), jobs))
    keep = [json.loads(l) for l in path.open()] if path.exists() else []
    keep = [k for k in keep if k["label"] != "INVALID"] + rows
    path.write_text("".join(json.dumps(k) + "\n" for k in keep))
    print(f"{len(rows)} new judge rows -> {path} ({sum(r['label'] == 'INVALID' for r in rows)} invalid)")
    summary(df, pd.DataFrame(keep))


def summary(df, runs, refs=("consensus", "claude", "gpt", "human")):
    ref = df[["case_id", "claude"]].copy()
    gp = sorted(D.glob("labels_gpt_*.csv"))
    if gp:
        ref = ref.merge(pd.read_csv(gp[-1])[["case_id", "gpt"]], on="case_id", how="left")
    if "gpt" in ref:                       # consensus: both labelers agree (disputed cases left out)
        ref["consensus"] = ref.claude.where(ref.claude == ref.gpt)
    hp = D / "review_justin.csv"
    if hp.exists():
        h = pd.read_csv(hp)
        h = h[h.intervene.astype(str).str.strip().isin(["0", "1"])]
        if len(h):
            ref = ref.merge(h[["case_id", "intervene"]].rename(columns={"intervene": "human"}), on="case_id", how="left")
            ref["human"] = pd.to_numeric(ref.human, errors="coerce")
    lines = []
    for cond, g in runs.groupby("condition"):
        g = g.drop_duplicates("case_id", keep="last").merge(ref, on="case_id")
        g["iv"] = (g.label == "INTERVENE").astype(int)
        row = {"condition": cond, "n": len(g), "INTERVENE": int(g.iv.sum()),
               "TRACK": int((g.label == "TRACK").sum())}
        for rcol in refs:
            if rcol in g and g[rcol].notna().any():
                s = g.dropna(subset=[rcol])
                pos, neg = s[s[rcol] == 1], s[s[rcol] == 0]
                row[f"catch_vs_{rcol}"] = f"{int(pos.iv.sum())}/{len(pos)}"
                row[f"false_alarm_vs_{rcol}"] = f"{int(neg.iv.sum())}/{len(neg)} ({neg.iv.mean():.0%})"
        lines.append(row)
    t = pd.DataFrame(lines)
    print(t.to_string(index=False))
    return t, ref


# ---------------------------------------------------------------- review
def cmd_review():
    df = load()
    gp = sorted(D.glob("labels_gpt_*.csv"))
    g = pd.read_csv(gp[-1]) if gp else pd.DataFrame({"case_id": df.case_id, "gpt": None, "gpt_conflict": ""})
    m = df.merge(g, on="case_id", how="left")
    pick = m[(m.claude == 1) | (m.gpt == 1) | (m.claude != m.gpt)]
    rest = m.drop(pick.index).sample(min(15, len(m) - len(pick)), random_state=0)
    sheet = pd.concat([pick, rest]).sample(frac=1, random_state=1)    # shuffled, labels hidden
    md = ["# Real-data label review", "", "For each case: should an AI teammate proactively intervene because the",
          "NEW message conflicts with, invalidates, or materially changes something said earlier?",
          "Write 1 (yes) or 0 (no) in data/real/review_justin.csv. Labels from Claude/GPT are not shown.", ""]
    for r in sheet.itertuples():
        ms = msgs(r.prior_context)
        md += [f"## {r.case_id}  ({len(ms)} earlier messages)", "", "```", *[fmt_msg(x) for x in ms], "```", "",
               f"> **NEW:** {fmt_msg(r.new_message.strip())}", "", "---", ""]
    (D / "review_sheet.md").write_text("\n".join(md))
    pd.DataFrame({"case_id": sheet.case_id, "intervene": "", "notes": ""}).to_csv(D / "review_justin.csv", index=False)
    print(f"{len(sheet)} cases ({len(pick)} positive or disputed + {len(rest)} random negatives) -> "
          f"{D/'review_sheet.md'}; fill {D/'review_justin.csv'}")


# ---------------------------------------------------------------- report
def cmd_report():
    df = load()
    runs = pd.DataFrame([json.loads(l) for l in (D / "judge_runs.jsonl").open()])
    t, ref = summary(df, runs)
    from sklearn.metrics import cohen_kappa_score
    s = ref.dropna(subset=["gpt"])
    both = s[(s.claude == 1) & (s.gpt == 1)].case_id.tolist()
    either = s[(s.claude == 1) | (s.gpt == 1)].case_id.tolist()
    iv_any = runs[runs.label == "INTERVENE"].case_id.unique().tolist()
    tr = runs[runs.label == "TRACK"].groupby("condition").case_id.nunique().to_dict()
    out = ["# Real-data check (aggregate only; the data is private)", "",
           "50 decision points from 10 real team-chat conversations between people and AI agents. Each case is",
           "one thread plus a new message, so this checks the judge on real chat; no cross-thread retrieval is involved.",
           "Same judge prompt and rubric as the benchmark.", "",
           "## Reference labels",
           f"- Claude first pass: {int(ref.claude.sum())}/50 should intervene; GPT labeler ({os.environ.get('LABELER_MODEL', 'gpt')}): "
           f"{int(s.gpt.sum())}/{len(s)}.",
           f"- Agreement {(s.claude == s.gpt).mean():.0%}, kappa {cohen_kappa_score(s.claude, s.gpt):.2f}: they agree on "
           f"{len(both)} positives ({', '.join(both)}); {len(either) - len(both)} more are flagged by only one.",
           "- Consensus reference = cases where both labelers agree (disputed cases excluded)."]
    if "human" in ref and ref.human.notna().any():
        h = ref.dropna(subset=["human"])
        out += [f"- Human check on {len(h)} cases: {int(h.human.sum())} positive."]
    out += ["", "## Judge on real chat", "", t.to_markdown(index=False), "",
            "FULL = whole thread shown; LAST15 = last 15 messages only; ~haiku / ~gpt = different judge model.",
            "catch = INTERVENE on reference-positive cases; false_alarm = INTERVENE on reference-negative cases.",
            f"TRACK given on: {tr}.", "",
            "## Findings",
            f"1. Real conflicts are ambiguous: two independent model labelers each mark about 10% of cases, but agree on "
            f"only {len(both)} (kappa {cohen_kappa_score(s.claude, s.gpt):.2f}), versus clean planted conflicts in the simulation.",
            f"2. The judge intervened on {len(iv_any)} of 50 cases under every condition (Sonnet, Haiku, GPT; full or truncated "
            f"thread): no false alarms, and it missed {('both' if len(both) == 2 else 'all ' + str(len(both))) if not set(both) & set(iv_any) else 'some'} "
            "consensus conflicts. A judge tuned for fact conflicts stays silent on these.",
            "3. The candidate conflicts concern the agents' own claims and work (promising actions they cannot take, "
            "contradicting their own earlier diagnosis, duplicate tickets from parallel agents), a category the simulated "
            "benchmark (people changing dates, owners and numbers) does not cover.", ""]
    Path("results/real_check.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[-6:]))
    print("-> results/real_check.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["label", "judge", "review", "report"])
    ap.add_argument("--conditions", default="FULL,LAST15,FULL~haiku,FULL~gpt")
    a = ap.parse_args()
    {"label": cmd_label, "review": cmd_review, "report": cmd_report}.get(a.cmd, lambda: cmd_judge(a.conditions.split(",")))()


if __name__ == "__main__":
    main()
