"""Score the paired conflict / control probes (verification item 1).

    python -m eval.score_probes        # -> results/probe_decisions.csv

Per condition: conflict catch rate (INTERVENE on the wrong-value message), control false-alarm rate
(INTERVENE on the same message with the current value), balanced accuracy, strict catch (cited value
names the current value), split by conflict kind (stale vs invented) and by delivery. 95% CIs by
bootstrap over FACTS (probes sharing a fact are resampled together). Paired differences vs B3.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from sim.run_workspace import load, vpat

RNG = np.random.default_rng(0)
B = 2000
DIR = Path("data/runs/probes")
POINTS = Path("data/probe_points.json")


def main():
    pts = {p["point_id"]: p for p in json.load(open(POINTS))}
    rows = []
    for f in sorted(DIR.glob("*_b*.jsonl")):
        for l in f.open():
            r = json.loads(l)
            p = pts.get(r["point_id"])
            if not p:
                continue
            rows.append({"cond": r["condition"], "pair": r["point_id"].split("#")[0], "kind": p["kind"],
                         "fact": f"{p['ws']}:{p['fact_id']}", "ws": p["ws"], "fact_id": p["fact_id"],
                         "current": p["current"], "ck": p["conflict_kind"], "form": p["origin_form"],
                         "iv": r["label"] == "INTERVENE", "label": r["label"], "delivery": r["delivery"],
                         "cited": r.get("cited_value", "")})
    df = pd.DataFrame(rows)
    if df.empty:
        print("no probe runs yet in", DIR)
        return
    ds = {ws: load(ws) for ws in df.ws.unique()}
    df["strict"] = [r.iv and bool(vpat(ds[r.ws], r.fact_id, r.current).search(r.cited or "")) for r in df.itertuples()]
    conf, ctrl = df[df.kind == "probe_conflict"], df[df.kind == "probe_control"]
    facts = sorted(df.fact.unique())

    def stat_ci(sub, col):
        g = sub.groupby("fact")[col].agg(["sum", "count"]).reindex(facts).fillna(0)
        s, n = g["sum"].values, g["count"].values
        bs = []
        for _ in range(B):
            ix = RNG.integers(0, len(facts), len(facts))
            bs.append(s[ix].sum() / max(n[ix].sum(), 1))
        return s.sum() / max(n.sum(), 1), *np.percentile(bs, [2.5, 97.5])

    out = []
    for c in sorted(df.cond.unique()):
        a, b = conf[conf.cond == c], ctrl[ctrl.cond == c]
        catch, clo, chi = stat_ci(a, "iv")
        fa, flo, fhi = stat_ci(b, "iv")
        row = {"condition": c, "n_pairs": len(a), "catch": catch, "catch_lo": clo, "catch_hi": chi,
               "false_alarm": fa, "fa_lo": flo, "fa_hi": fhi, "bal_acc": (catch + 1 - fa) / 2,
               "strict_catch": a.strict.mean()}
        for k in ("stale", "invented"):
            row[f"catch_{k}"] = a[a.ck == k].iv.mean()
        full = a[a.delivery == "full"]; notfull = a[a.delivery.isin(["none", "partial"])]
        row["catch|full"] = full.iv.mean() if len(full) else np.nan
        row["catch|not_full"] = notfull.iv.mean() if len(notfull) else np.nan
        row["delivered_full"] = (a.delivery == "full").mean() if (a.delivery != "n/a").any() else np.nan
        out.append(row)
    res = pd.DataFrame(out)
    order = ["S0", "A3", "B3", "Cs2", "D2", "E1", "AG-grep", "OR"]
    res = res.sort_values("condition", key=lambda s: s.map(lambda x: (order.index(x) if x in order else 99, x)))
    res.round(3).to_csv("results/probe_decisions.csv", index=False)
    show = res.copy()
    for col in ("catch", "false_alarm"):
        lo, hi = ("catch_lo", "catch_hi") if col == "catch" else ("fa_lo", "fa_hi")
        show[col] = [f"{100*v:.0f} [{100*l:.0f}, {100*h:.0f}]" for v, l, h in zip(show[col], show[lo], show[hi])]
    for col in ("bal_acc", "strict_catch", "catch_stale", "catch_invented", "catch|full", "catch|not_full", "delivered_full"):
        show[col] = (100 * show[col]).round(0)
    print(show[["condition", "n_pairs", "catch", "false_alarm", "bal_acc", "strict_catch", "catch_stale",
                "catch_invented", "delivered_full", "catch|full", "catch|not_full"]].to_string(index=False))

    # paired differences in catch rate vs B3 and vs E1 (same pairs), bootstrap over facts
    piv = conf.pivot_table(index=["fact", "pair"], columns="cond", values="iv", aggfunc="first").astype(float)
    print("\nPaired catch-rate differences (pts, 95% CI, resampling facts):")
    fidx = piv.index.get_level_values(0)
    groups = {f: piv.loc[f] for f in fidx.unique()}
    flist = list(groups)
    for ref in ("B3", "E1"):
        if ref not in piv:
            continue
        for c in piv.columns:
            if c == ref:
                continue
            d = (piv[c] - piv[ref]).dropna()
            obs = d.mean()
            bs = []
            for _ in range(B):
                ix = RNG.integers(0, len(flist), len(flist))
                sub = pd.concat([(groups[flist[i]][c] - groups[flist[i]][ref]) for i in ix]).dropna()
                bs.append(sub.mean())
            lo, hi = np.percentile(bs, [2.5, 97.5])
            flag = "" if lo <= 0 <= hi else "  *"
            print(f"  {c:<8} - {ref:<3} {100*obs:+5.1f}  [{100*lo:+.1f}, {100*hi:+.1f}]{flag}")
    print("\n* = CI excludes 0.  -> results/probe_decisions.csv")


if __name__ == "__main__":
    main()
