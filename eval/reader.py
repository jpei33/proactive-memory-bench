"""Layer 1b: given what memory delivered, can a fixed reader answer the probe correctly? (3.7)

    python -m eval.reader --out results/probes.csv           # ~720 Sonnet calls, cached
    python -m eval.reader --show wrong --n 20                # hand-check rows

For every fact plant (all are INTERVENE types) x condition (6 chunkers x 3 retrievers, window, oracle):
retrieve with the plant's probe (reactive mode, budget 1500), show the reader the recent window +
retrieved memory, and ask "answer using ONLY the memory; else UNKNOWN".
Scoring:
  fact plants (have fact_id): regex on the answer. gold value -> correct; an earlier value -> stale;
     UNKNOWN / nothing -> missing; any other answer -> wrong.
  item plants (deadline_passed, gold "not done"): a cheap grader (Haiku) reads the answer:
     says not done / no sign it was done -> correct; says done -> wrong; UNKNOWN -> missing.
Each row also keeps the retrieval delivery, so you can see if delivery=full actually yields a correct
answer (E's statements could be delivered but wrong).
"""
from __future__ import annotations

import argparse
import csv
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from memory.base import deliveries, line, load_msgs, make_chunk, visible
from memory.build import CHUNKERS, build_chunks
from memory.retrievers import RANKERS, prefetch, retrieve
from eval.retrieval_grid import queries
from sim.run_workspace import load, vpat

READER = """You are an AI teammate in a company chat. Answer the question using ONLY the memory below.
If the memory does not contain the answer, reply exactly UNKNOWN.

MEMORY (retrieved notes and recent messages):
{MEMORY}

QUESTION: {QUESTION}{EXTRA}
Answer in one short sentence."""

ITEM_HINT = """
(For an "Is this done" question: if the memory records the task or commitment but nothing shows it was
completed, answer "Not done" and cite the commitment. Say UNKNOWN only if the task is not in memory.)"""

GRADE = """A teammate was asked: "{QUESTION}"
They answered: "{ANSWER}"
Reply with one word:
NOT_DONE  if it says the task is not done, or cites the task/commitment and says nothing shows it was done
DONE      if it says the task was done
UNKNOWN   if it says the task is not in memory at all, or gives no view"""

WSS = ["ando", "anthropic", "openai", "xai"]
COLS = ["ws", "plant_id", "type", "chunker", "retriever", "delivery", "outcome", "answer",
        "evidence_form", "restated", "bucket", "structure"]


def says_unknown(a: str) -> bool:
    """UNKNOWN as the answer: first word, or the final line/word after some hedging."""
    a = a.strip().strip("*").strip()
    last = a.splitlines()[-1].strip().strip("*.").strip() if a else ""
    return (not a or a.upper().startswith("UNKNOWN") or last.upper() == "UNKNOWN"
            or a.rstrip("*. ").upper().endswith("UNKNOWN"))


def score_fact(d, p, answer):
    a = answer.strip()
    if says_unknown(a):
        return "missing"
    if vpat(d, p["fact_id"], p["gold_value"]).search(a):
        return "correct"
    f = d["_fact"][p["fact_id"]]
    if any(h["value"] != p["gold_value"] and vpat(d, p["fact_id"], h["value"]).search(a) for h in f["history"]):
        return "stale"
    return "wrong"


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/probes.csv")
    ap.add_argument("--budget", type=int, default=1500)
    ap.add_argument("--show", choices=["wrong", "stale", "missing", "correct"])
    ap.add_argument("--n", type=int, default=20)
    a = ap.parse_args()
    if a.show:
        import pandas as pd
        df = pd.read_csv(a.out, keep_default_na=False)
        s = df[df.outcome == a.show].sample(min(a.n, (df.outcome == a.show).sum()), random_state=0)
        for _, r in s.iterrows():
            print(f"{r.plant_id} [{r.chunker}/{r.retriever}, delivery={r.delivery}] -> {r.answer}")
        return

    from sim.llm import complete
    judge = os.environ.get("JUDGE_MODEL")
    cheap = os.environ.get("CHEAP_JUDGE_MODEL", "claude-haiku-4-5-20251001")
    jobs = []
    for ws in WSS:
        msgs, d = load_msgs(ws), load(ws)
        by_id = {m["msg_id"]: m for m in msgs}
        qs = [q for q in queries(ws, msgs, by_id, d) if q["query_kind"] == "plant" and q["mode"] == "reactive"]
        built = {c: build_chunks(ws, c, msgs) for c in CHUNKERS}
        vis = {(i, c): [ch for ch in visible(built[c], q["q_seq"], by_id) if not set(ch.source_msgs) <= set(q["win_ids"])]
               for i, q in enumerate(qs) for c in CHUNKERS}
        prefetch(list({ch.text for v in vis.values() for ch in v}), "d")
        prefetch([q["q"] for q in qs], "q")
        for i, q in enumerate(qs):
            p = q["plant"]
            win_txt = "\n".join(line(by_id[m]) for m in q["win_ids"])
            conds = [("window", "-", [])]
            orc = [make_chunk(f"O:{g['group']}", [by_id[m] for m in g["msgs"]]) for g in p["evidence_groups"]]
            conds.append(("oracle", "-", visible(orc, q["q_seq"], by_id)))
            conds += [(c, r, retrieve(vis[i, c], q["q"], r, a.budget)) for c in CHUNKERS for r in RANKERS]
            for c, r, got in conds:
                mem = "\n".join(ch.text for ch in got)
                memory = (mem + "\n--- recent messages ---\n" if mem else "") + win_txt
                jobs.append((ws, d, q, p, c, r, deliveries(got, q["win_ids"], p)["all"],
                             READER.replace("{MEMORY}", memory).replace("{QUESTION}", p["probe"])
                             .replace("{EXTRA}", "" if p.get("fact_id") else ITEM_HINT)))
    print(f"{len(jobs)} reader calls (cached ones are free)")

    def run(job):
        ws, d, q, p, c, r, dl, prompt = job
        r_ = complete(None, prompt, model=judge, max_tokens=2000, effort="low")
        ans = r_.text.strip()
        if r_.stop_reason == "max_tokens":
            ans = ans or "[TRUNCATED]"
        if ans == "[TRUNCATED]":
            out = "error"                      # reader ran out of tokens; should be ~0 rows
        elif p.get("fact_id"):
            out = score_fact(d, p, ans)
        else:                                  # "UNKNOWN, nothing shows it was sent" = not done: let the grader decide
            g = complete(None, GRADE.replace("{QUESTION}", p["probe"]).replace("{ANSWER}", ans),
                         model=cheap, max_tokens=5).text.strip().upper()
            out = "correct" if g.startswith("NOT") else "wrong" if g.startswith("DONE") else "missing"
        return {"ws": ws, "plant_id": p["plant_id"], "type": p["type"], "chunker": c, "retriever": r,
                "delivery": dl, "outcome": out, "answer": ans, "evidence_form": q["evidence_form"],
                "restated": q["restated"], "bucket": q["bucket"], "structure": q["structure"]}

    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(run, jobs))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    import pandas as pd
    df = pd.DataFrame(rows)
    df["cond"] = df.chunker + df.retriever.map(lambda r: "" if r == "-" else f"/{r}")
    t = pd.crosstab(df.cond, df.outcome, normalize="index").mul(100).round()
    order = ["window"] + [f"{c}/{r}" for c in CHUNKERS for r in RANKERS] + ["oracle"]
    print("\n% of plants by reader outcome")
    print(t.reindex(order).fillna(0).astype(int).to_string())
    print("\ncorrect | delivery (all conditions): " + ", ".join(
        f"{k}={round(100 * (g.outcome == 'correct').mean())}% (n={len(g)})" for k, g in df.groupby("delivery")))
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
