"""Step 8: do the 3-way memory arms change the judge's decisions? (Sonnet judge, paired probes)

    python -m eval.threeway_decisions     # -> results/threeway_decisions.csv (no API calls)

Reads the Sonnet probe runs in data/runs/probes/ (untagged = JUDGE_MODEL): S0 (no memory), D4 (arm 1),
Z4 (arm 1z), E1 (arm 3), plus B3 / D2 / OR as references when present. L4 if it was run.
Per condition: catch rate on the 142 conflict probes, false-alarm rate on the 142 controls, and
balanced accuracy = (catch + 1 - false_alarm) / 2. Paired differences vs D4 and vs E1 on the same
probes. 95% CIs: bootstrap over facts (all probes sharing a fact are resampled together).
Also: catch rate when the memory delivered the full evidence vs not (delivery comes from retrieval,
so it is judge-independent).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

CONDS = ["S0", "D2", "B3", "D4", "Z4", "L4", "E1", "OR"]
B = 2000
RNG = np.random.default_rng(0)


def load():
    pts = {p["point_id"]: p for p in json.load(open("data/probe_points.json"))}
    rows = []
    for c in CONDS:
        f = Path(f"data/runs/probes/{c}_b1500.jsonl")
        if not f.exists():
            continue
        for l in f.open():
            r = json.loads(l)
            p = pts.get(r["point_id"])
            if p and r["label"] != "INVALID":
                rows.append({"cond": c, "point_id": r["point_id"], "fact": f"{p['ws']}:{p['fact_id']}",
                             "kind": p["kind"], "iv": float(r["label"] == "INTERVENE"),
                             "full": r["delivery"] == "full"})
    return pd.DataFrame(rows)


def stats(d, conds):
    g = d.groupby(["cond", "kind"]).iv.mean()
    out = {}
    for c in conds:
        ca, fa = g.get((c, "probe_conflict"), np.nan), g.get((c, "probe_control"), np.nan)
        out[c] = (ca, fa, (ca + 1 - fa) / 2)
    return out


def main():
    df = load()
    conds = [c for c in CONDS if c in set(df.cond)]
    n = df.groupby("cond").size()
    facts = df.fact.unique()
    groups = {f: g for f, g in df.groupby("fact")}
    obs = stats(df, conds)
    bs = [stats(pd.concat([groups[f] for f in RNG.choice(facts, len(facts))]), conds) for _ in range(B)]
    rows = []
    print(f"Sonnet judge, paired probes ({n.max()} points per condition; 95% CI over {len(facts)} facts)\n")
    print(f"{'cond':<5}{'catch':>16}{'false alarm':>18}{'bal. acc':>18}   catch|full  catch|not full")
    for c in conds:
        ci = lambda k: np.nanpercentile([b[c][k] for b in bs], [2.5, 97.5]) * 100
        (lo0, hi0), (lo1, hi1), (lo2, hi2) = ci(0), ci(1), ci(2)
        conf = df[(df.cond == c) & (df.kind == "probe_conflict")]
        cf = conf[conf.full].iv.mean() * 100 if conf.full.any() else np.nan
        cn = conf[~conf.full].iv.mean() * 100 if (~conf.full).any() else np.nan
        ca, fa, ba = (100 * x for x in obs[c])
        rows.append({"cond": c, "n": int(n[c]), "catch": ca, "catch_lo": lo0, "catch_hi": hi0, "false_alarm": fa,
                     "fa_lo": lo1, "fa_hi": hi1, "bal_acc": ba, "bal_lo": lo2, "bal_hi": hi2,
                     "catch_given_full": cf, "catch_given_not_full": cn})
        print(f"{c:<5}{ca:6.1f} [{lo0:4.0f},{hi0:4.0f}]{fa:8.1f} [{lo1:4.0f},{hi1:4.0f}]{ba:8.1f} [{lo2:4.0f},{hi2:4.0f}]"
              f"   {cf:8.1f}   {cn:8.1f}")
    print("\npaired differences in balanced accuracy (pts, 95% CI; * = excludes 0):")
    for ref in ("D4", "E1"):
        if ref not in conds:
            continue
        for c in conds:
            if c == ref:
                continue
            d = np.array([b[c][2] - b[ref][2] for b in bs]) * 100
            o = (obs[c][2] - obs[ref][2]) * 100
            lo, hi = np.nanpercentile(d, [2.5, 97.5])
            print(f"  {c:<3} - {ref}  {o:+5.1f} [{lo:+5.1f},{hi:+5.1f}]{' *' if lo > 0 or hi < 0 else ''}")
            rows.append({"cond": f"{c}-{ref}", "bal_acc": o, "bal_lo": lo, "bal_hi": hi})
    pd.DataFrame(rows).round(2).to_csv("results/threeway_decisions.csv", index=False)
    print("\n-> results/threeway_decisions.csv")


if __name__ == "__main__":
    main()
