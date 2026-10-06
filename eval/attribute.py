"""Attribute every missed INTERVENE plant to one cause, per condition (5.2).

    python -m eval.attribute         # -> results/attribution.csv (counts), results/attribution_rows.csv (per miss)

A plant is missed when the judge did not INTERVENE at the trigger or the next k=2 channel messages.
Cause, first match wins:
  lost_in_chunking   even the probe question (reactive query) can't retrieve the full evidence
  split_evidence     at the trigger, only part of the evidence reached the judge ("I'll take it" w/o its question)
  not_surfaced       findable when asked, but the trigger's query pulled none of it
  stale_in_memory    evidence delivered, but the memory shown also contains the outdated value
  not_acted_on       evidence delivered (or oracle), the judge still said TRACK or IGNORE
Agentic arms have no fixed retrieval, so for them lost_in_chunking doesn't apply.
Over-triggers (INTERVENE on gold-IGNORE core points) are counted separately by point kind / decoy type.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

from eval.score import cell, cites, load_runs, plant_table

CAUSES = ["lost_in_chunking", "split_evidence", "not_surfaced", "stale_in_memory",
          "not_acted_on (said TRACK)", "not_acted_on (said IGNORE)"]


def main():
    runs = load_runs()
    plants = plant_table()
    iv = [p for p in plants if p["gold_label"] == "INTERVENE"]
    points = {p["point_id"]: p for p in json.load(open("data/eval_points.json"))}
    gold = {g["point_id"]: g for g in json.load(open("data/gold/labels.json"))}
    after = defaultdict(list)
    for pt in points.values():
        if pt["kind"] == "plant_after":
            after[pt["plant_id"]].append(pt["point_id"])
    grid = pd.read_csv("results/retrieval_grid.csv", keep_default_na=False)
    react = grid[(grid["mode"] == "reactive") & (grid.query_kind == "plant")]
    react = {(r.chunker, r.retriever, r.query_id): r.delivery for r in react.itertuples()}
    decoy_type = {p["plant_id"]: p["type"] for p in plants}
    for ws in ("ando", "anthropic", "openai", "xai"):
        for l in Path(f"data/workspaces/{ws}/plants.jsonl").read_text().splitlines():
            p = json.loads(l)
            decoy_type[p["plant_id"]] = p["type"]

    rows, counts, over = [], [], []
    for cond, g in runs.groupby("cond"):
        g = g.drop_duplicates("point_id", keep="last").set_index("point_id")
        base = cond.split("@")[0].split("~")[0].split("+")[0]
        ck = cell(base)
        if ck:
            rkey = ck
        elif base == "S0":
            rkey = ("window", "-")
        elif base == "OR":
            rkey = ("oracle", "-")
        else:
            rkey = None                                   # agentic
        c = Counter()
        for p in iv:
            trig = p["trigger_msg"]
            if trig not in g.index:
                continue
            ids = [trig] + [a for a in after[p["plant_id"]] if a in g.index]
            if any(g.at[i, "label"] == "INTERVENE" for i in ids):
                continue
            dl = g.at[trig, "delivery"]
            rd = react.get((*rkey, p["plant_id"])) if rkey else None
            mem = g.at[trig, "memory_text"] or ""
            lab = g.at[trig, "label"]
            if base != "OR" and rd == "none":
                cause = "lost_in_chunking"
            elif dl == "partial":
                cause = "split_evidence"
            elif dl == "none":
                cause = "not_surfaced"
            elif p.get("fact_id") and any(cites(p["_d"], p["fact_id"], s, mem) for s in p["stale_values"]):
                cause = "stale_in_memory"
            else:
                cause = f"not_acted_on (said {lab})"
            c[cause] += 1
            rows.append({"condition": cond, "plant_id": p["plant_id"], "type": p["type"],
                         "form": p.get("evidence_form"), "bucket": p.get("bucket"), "structure": p.get("structure"),
                         "cause": cause, "delivery": dl, "reactive_delivery": rd, "label_at_trigger": lab,
                         "reason": g.at[trig, "reason"], "memory_text": mem})
        for cause in CAUSES:
            counts.append({"condition": cond, "cause": cause, "n": c.get(cause, 0)})
        counts.append({"condition": cond, "cause": "TOTAL_MISSES", "n": sum(c.values())})
        # over-triggers on core points
        for pid in g.index:
            pt = points.get(pid, {})
            if pt.get("kind") == "plant_after" or g.at[pid, "label"] != "INTERVENE":
                continue
            if gold.get(pid, {}).get("label") == "IGNORE":
                kind = pt.get("kind")
                over.append({"condition": cond, "kind": decoy_type.get(pt.get("plant_id"), kind) if kind == "decoy_trigger" else kind})

    cnt = pd.DataFrame(counts)
    cnt.to_csv("results/attribution.csv", index=False)
    pd.DataFrame(rows).to_csv("results/attribution_rows.csv", index=False)
    # check: causes sum to misses
    tot = cnt[cnt.cause == "TOTAL_MISSES"].set_index("condition").n
    summ = cnt[cnt.cause != "TOTAL_MISSES"].groupby("condition").n.sum()
    assert (tot == summ).all(), "cause counts don't sum to misses"

    order = ["S0"] + [f"{c}{k}" for c in "ABCDE" for k in "123"] + ["E1@500", "E1@4000", "Cs2", "AG-grep", "AG-both", "OR"]
    piv = cnt.pivot(index="condition", columns="cause", values="n").reindex([o for o in order if o in set(cnt.condition)])
    piv = piv[["TOTAL_MISSES"] + CAUSES]
    piv.columns = ["misses", "lost", "split", "not_surf", "stale", "acted:TRACK", "acted:IGNORE"]
    print("Missed INTERVENE plants (of 36) by cause:")
    print(piv.to_string())
    agg = defaultdict(Counter)
    for o in over:
        agg[o["condition"]][o["kind"]] += 1
    ov = pd.DataFrame(agg).T.fillna(0).astype(int).reindex([o for o in order if o in agg])
    print("\nOver-triggers (INTERVENE on gold IGNORE, core points) by point kind / decoy type:")
    print(ov.to_string())
    print("\n-> results/attribution.csv, results/attribution_rows.csv (every miss, with what the judge saw)")


if __name__ == "__main__":
    main()
