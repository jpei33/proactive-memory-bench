"""Score every judged condition (5.1).

    python -m eval.score                      # -> results/main.csv, results/by_slice.csv, results/grid_stats.csv

Inputs: data/runs/<cond>_b<budget>.jsonl (judge decisions), data/gold/labels.json (gold label per point),
plants (with audited restatements), results/retrieval_grid.csv (L1/L2 for grid cells), results/probes.csv (L1b).

Per condition (main.csv)
  n_points            points judged so far (partial runs are scored on what exists)
  acc, macro_f1       vs gold labels over all judged points
  iv_prec/rec/f1      INTERVENE vs gold labels (95% CI on f1, bootstrap over points)
  L1_reactive         % INTERVENE fact plants with full delivery when queried with the probe (grid only)
  L1b_correct         % reader answers correct (probes.csv; grid, window, oracle)
  L2_full/partial     % INTERVENE fact plants whose evidence reached the judge at the trigger
  L3_loose            % INTERVENE plants with INTERVENE at the trigger or the next k=2 channel messages (95% CI)
  L3_strict           loose + cited_value names the current value (fact plants)
  capture_given_full  L3 loose among plants with L2 full
  n_core              points scored for decisions: all except plant_after (those only feed the k=2 window)
  false_per100        100 x sum severity of INTERVENE on gold IGNORE / n_core
  repeat_after        share of IV plants flagged more than once in the trigger + k window (stateless judge)
  stale_per100        100 x INTERVENE citing an outdated value (and not the current one) / n_points
  track_success       TRACK at the commitment and (if it has one) INTERVENE once its deadline passed
  tool_use_rate       share of points with >= 1 tool call (agentic arms)
  usd_per_1k          judge tokens priced (batch or live) + write-time cost of the chunker, per 1,000 decisions
  lat_p50/p95         live calls only
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from memory.base import load_plants
from sim.run_workspace import load, vpat

WSS = ["ando", "anthropic", "openai", "xai"]
RUNS = Path("data/runs")
RNG = np.random.default_rng(0)
B = 1000
CHUNK = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "Cs": "Cstar"}
RET = {"1": "bm25", "2": "emb", "3": "rrf"}
# write-time cost of building each memory for the whole corpus (Haiku, from eval/estimate_cost.py)
WRITE_USD = {"E": 0.44, "C": 0.22, "D": 0.04}


def cell(cond):
    cond = cond.split("~")[0].split("+")[0]
    if cond in ("S0", "OR") or cond.startswith("AG-"):
        return None
    return CHUNK[cond[:-1]], RET[cond[-1]]


def load_runs():
    rows = []
    for f in sorted(RUNS.glob("*_b*.jsonl")):
        for l in f.open():
            r = json.loads(l)
            rows.append(r)
    df = pd.DataFrame(rows)
    df["cond"] = df.condition + np.where(df.budget == 1500, "", "@" + df.budget.astype(str))
    return df


def macro_f1(y, p):
    fs = []
    for c in ("IGNORE", "TRACK", "INTERVENE"):
        tp = ((y == c) & (p == c)).sum(); fp = ((y != c) & (p == c)).sum(); fn = ((y == c) & (p != c)).sum()
        fs.append(2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0)
    return float(np.mean(fs))


def iv_prf(y, p):
    tp = ((y == "INTERVENE") & (p == "INTERVENE")).sum()
    fp = ((y != "INTERVENE") & (p == "INTERVENE")).sum()
    fn = ((y == "INTERVENE") & (p != "INTERVENE")).sum()
    pr = tp / (tp + fp) if tp + fp else 0.0
    rc = tp / (tp + fn) if tp + fn else 0.0
    return pr, rc, (2 * pr * rc / (pr + rc) if pr + rc else 0.0)


def ci(values_fn, n):
    """95% bootstrap CI of a statistic over n resampled units."""
    stats = [values_fn(RNG.integers(0, n, n)) for _ in range(B)]
    return np.percentile(stats, [2.5, 97.5])


def plant_table():
    """One row per plant with the info scoring needs."""
    out = []
    for ws in WSS:
        d = load(ws)
        for p in load_plants(ws):
            if p["kind"] != "plant":
                continue
            stale = []
            if p.get("fact_id"):
                stale = [h["value"] for h in d["_fact"][p["fact_id"]]["history"] if h["value"] != p["gold_value"]]
            out.append({**p, "ws": ws, "_d": d, "stale_values": stale})
    return out


def cites(d, fact, value, text):
    try:
        return bool(vpat(d, fact, value).search(text or ""))
    except Exception:
        return False


def main():
    runs = load_runs()
    gold = {g["point_id"]: g for g in json.load(open("data/gold/labels.json"))}
    points = {p["point_id"]: p for p in json.load(open("data/eval_points.json"))}
    plants = plant_table()
    by_plant = {p["plant_id"]: p for p in plants}
    after = defaultdict(list)                       # plant_id -> its k=2 follow-up point ids
    for pt in points.values():
        if pt["kind"] == "plant_after":
            after[pt["plant_id"]].append(pt["point_id"])
    grid = pd.read_csv("results/retrieval_grid.csv", keep_default_na=False) if Path("results/retrieval_grid.csv").exists() else None
    probes = pd.read_csv("results/probes.csv", keep_default_na=False) if Path("results/probes.csv").exists() else None
    prices = {k: v for k, v in json.load(open("eval/prices.json")).items() if not k.startswith("_")}
    import os
    from dotenv import load_dotenv
    load_dotenv(".env")
    jp = next(v for k, v in prices.items() if os.environ.get("JUDGE_MODEL", "claude-sonnet-5-5").startswith(k))

    main_rows, slice_rows = [], []
    iv_plants = [p for p in plants if p["gold_label"] == "INTERVENE"]
    tr_plants = [p for p in plants if p["gold_label"] == "TRACK"]

    for cond, g in runs.groupby("cond"):
        g = g.drop_duplicates("point_id", keep="last").set_index("point_id")
        lab = g.label
        # Decision metrics exclude plant_after points: they exist only for the k=2 capture window.
        # The judge is stateless, so after catching a conflict it often flags it again on the next
        # message; counting those as false alarms would punish the conditions that caught it.
        core = [pid for pid in g.index if pid in gold and points.get(pid, {}).get("kind") != "plant_after"]
        y = pd.Series({pid: gold[pid]["label"] for pid in core})
        p_ = lab.reindex(y.index)
        n = len(y)
        r = {"condition": cond, "n_points": len(g), "n_core": n}
        r["acc"] = round(float((y == p_).mean()), 3)
        r["macro_f1"] = round(macro_f1(y.values, p_.values), 3)
        pr, rc, f1 = iv_prf(y.values, p_.values)
        lo, hi = ci(lambda ix: iv_prf(y.values[ix], p_.values[ix])[2], n)
        r.update(iv_prec=round(pr, 3), iv_rec=round(rc, 3), iv_f1=round(f1, 3), iv_f1_lo=round(lo, 3), iv_f1_hi=round(hi, 3))

        # ---- plant-level capture (L2, L3)
        caps = []
        for p in iv_plants:
            trig = p["trigger_msg"]
            if trig not in g.index:
                continue
            ids = [trig] + [a for a in after[p["plant_id"]] if a in g.index]
            hit = [i for i in ids if g.at[i, "label"] == "INTERVENE"]
            loose = bool(hit)
            strict = loose and (not p.get("fact_id") or any(cites(p["_d"], p["fact_id"], p["gold_value"], g.at[i, "cited_value"]) for i in hit))
            dl = g.at[trig, "delivery"] if "delivery" in g.columns else "n/a"
            caps.append({"plant_id": p["plant_id"], "loose": loose, "strict": strict, "late": loose and trig not in hit,
                         "repeat": len(hit) > 1,
                         "delivery": dl, "form": p.get("evidence_form"), "restated": bool(p.get("restated")),
                         "bucket": p.get("bucket"), "structure": p.get("structure"), "type": p["type"]})
        c = pd.DataFrame(caps)
        if len(c):
            r["n_iv_plants"] = len(c)
            r["L3_loose"] = round(c.loose.mean(), 3)
            lo, hi = ci(lambda ix: c.loose.values[ix].mean(), len(c))
            r.update(L3_loose_lo=round(lo, 3), L3_loose_hi=round(hi, 3))
            r["L3_strict"] = round(c.strict.mean(), 3)
            r["late_share"] = round(c.late.mean(), 3)
            r["repeat_after"] = round(c.repeat.mean(), 3)
            fact = c[c.delivery != "n/a"]
            if len(fact):
                r["L2_full"] = round((fact.delivery == "full").mean(), 3)
                r["L2_partial"] = round((fact.delivery == "partial").mean(), 3)
                full = fact[fact.delivery == "full"]
                r["capture_given_full"] = round(full.loose.mean(), 3) if len(full) else None
            for col in ("form", "bucket", "structure", "type"):
                for v, s in c.groupby(col):
                    slice_rows.append({"condition": cond, "slice": col, "value": v, "subset": "all", "n": len(s),
                                       "L3_loose": round(s.loose.mean(), 3),
                                       "L2_full": round((s.delivery == "full").mean(), 3) if (s.delivery != "n/a").any() else None})
            for v, s in c[~c.restated].groupby("form"):
                slice_rows.append({"condition": cond, "slice": "form", "value": v, "subset": "clean", "n": len(s),
                                   "L3_loose": round(s.loose.mean(), 3),
                                   "L2_full": round((s.delivery == "full").mean(), 3) if (s.delivery != "n/a").any() else None})

        # ---- false / stale interventions
        iv = g.loc[[i for i in g.index if i in set(core) and g.at[i, "label"] == "INTERVENE"]]
        false_sev = sum((iv.at[i, "severity"] or 1) for i in iv.index if gold.get(i, {}).get("label") == "IGNORE")
        r["false_per100"] = round(100 * false_sev / max(n, 1), 1)
        stale = 0
        for i in iv.index:
            pid = points.get(i, {}).get("plant_id")
            p = by_plant.get(pid)
            if p and p.get("fact_id") and p["stale_values"]:
                t = iv.at[i, "cited_value"]
                if any(cites(p["_d"], p["fact_id"], s, t) for s in p["stale_values"]) and not cites(p["_d"], p["fact_id"], p["gold_value"], t):
                    stale += 1
        r["stale_per100"] = round(100 * stale / max(n, 1), 1)

        # ---- TRACK success
        succ = []
        for p in tr_plants:
            if p["trigger_msg"] not in g.index:
                continue
            ok = g.at[p["trigger_msg"], "label"] == "TRACK"
            dl = [q for q in plants if q["type"] == "deadline_passed" and q.get("item_id") == p.get("item_id")]
            for q in dl:
                if q["trigger_msg"] in g.index:
                    ids = [q["trigger_msg"]] + [a for a in after[q["plant_id"]] if a in g.index]
                    ok = ok and any(g.at[i, "label"] == "INTERVENE" for i in ids)
            succ.append(ok)
        r["track_success"] = round(float(np.mean(succ)), 3) if succ else None

        # ---- L1 from the retrieval grid and the reader
        ck = cell(cond.split("@")[0])
        if grid is not None:
            gsel = None
            if ck:
                gsel = grid[(grid.chunker == ck[0]) & (grid.retriever == ck[1])]
            elif cond.split("~")[0] in ("S0", "OR"):
                gsel = grid[grid.chunker == ("window" if cond.startswith("S0") else "oracle")]
            if gsel is not None:
                re_ = gsel[(gsel["mode"] == "reactive") & (gsel.query_kind == "plant")]
                r["L1_reactive"] = round((re_.delivery == "full").mean(), 3) if len(re_) else None
        if probes is not None:
            if ck:
                ps = probes[(probes.chunker == ck[0]) & (probes.retriever == ck[1])]
            elif cond.split("~")[0] in ("S0", "OR"):
                ps = probes[probes.chunker == ("window" if cond.startswith("S0") else "oracle")]
            else:
                ps = probes.iloc[0:0]
            r["L1b_correct"] = round((ps.outcome == "correct").mean(), 3) if len(ps) else None

        # ---- tools, cost, latency
        if "tool_calls" in g.columns:
            r["tool_use_rate"] = round(float((g.tool_calls.fillna(0) > 0).mean()), 3) if cond.startswith("AG-") else None
        batch = g["batch_id"].notna() if "batch_id" in g.columns else pd.Series(False, index=g.index)
        tin, tout = g.in_tok.fillna(0), g.out_tok.fillna(0)
        tcr = g.cache_read_tok.fillna(0) if "cache_read_tok" in g.columns else 0
        jp_ = prices.get("claude-haiku-4-5") if "~haiku" in cond else jp
        usd = np.where(batch, tin * jp_["batch_in"] + tout * jp_["batch_out"], tin * jp_["in"] + tout * jp_["out"]).sum()
        usd += (tcr * jp_["cache_read"]).sum()
        usd = usd / 1e6
        write = WRITE_USD.get(ck[0], 0) if ck else 0
        r["usd_per_1k"] = round(1000 * (usd + write * len(g) / 303) / max(len(g), 1), 2)
        live = g[~batch & ~g.get("cached", pd.Series(False, index=g.index)).fillna(False).astype(bool)]
        if len(live) and "latency_s" in live and live.latency_s.notna().any():
            r["lat_p50"] = round(float(live.latency_s.dropna().median()), 2)
            r["lat_p95"] = round(float(live.latency_s.dropna().quantile(.95)), 2)
        main_rows.append(r)

    main_df = pd.DataFrame(main_rows)
    order = {c: i for i, c in enumerate(["S0"] + [f"{c}{k}" for c in "ABCDE" for k in "123"] +
                                         ["Cs1", "Cs2", "Cs3", "AG-grep", "AG-both", "OR"])}
    main_df = main_df.sort_values("condition", key=lambda s: s.map(lambda x: (order.get(x.split("@")[0], 99), x)))
    Path("results").mkdir(exist_ok=True)
    main_df.to_csv("results/main.csv", index=False)
    pd.DataFrame(slice_rows).to_csv("results/by_slice.csv", index=False)
    grid_stats()

    show = ["condition", "n_core", "macro_f1", "iv_f1", "iv_rec", "L2_full", "L3_loose", "L3_strict",
            "capture_given_full", "false_per100", "repeat_after", "track_success", "usd_per_1k"]
    print(main_df[[c for c in show if c in main_df.columns]].to_string(index=False))
    sanity(main_df, pd.DataFrame(slice_rows))


def grid_stats():
    """Row vs column spread of the L2 grid with bootstrap CIs; disentanglement gap Cstar - C by structure."""
    if not Path("results/retrieval_grid.csv").exists():
        return
    df = pd.read_csv("results/retrieval_grid.csv", keep_default_na=False)
    df = df[(df["mode"] == "proactive") & (df.chunker.isin(list("ABCDE")))]
    df["full"] = (df.delivery == "full").astype(float)
    w = df.pivot_table(index=["ws", "query_id"], columns=["chunker", "retriever"], values="full")
    def spreads(ix):
        m = w.iloc[ix].mean()
        rows = m.groupby(level=0).mean(); cols = m.groupby(level=1).mean()
        return rows.max() - rows.min(), cols.max() - cols.min()
    obs = spreads(np.arange(len(w)))
    bs = np.array([spreads(RNG.integers(0, len(w), len(w))) for _ in range(B)])
    out = [{"stat": "row_spread (chunkers)", "value": obs[0], "lo": np.percentile(bs[:, 0], 2.5), "hi": np.percentile(bs[:, 0], 97.5)},
           {"stat": "col_spread (retrievers)", "value": obs[1], "lo": np.percentile(bs[:, 1], 2.5), "hi": np.percentile(bs[:, 1], 97.5)},
           {"stat": "row - col", "value": obs[0] - obs[1], "lo": np.percentile(bs[:, 0] - bs[:, 1], 2.5),
            "hi": np.percentile(bs[:, 0] - bs[:, 1], 97.5)}]
    g2 = pd.read_csv("results/retrieval_grid.csv", keep_default_na=False)
    g2 = g2[(g2["mode"] == "proactive") & g2.chunker.isin(["C", "Cstar"])]
    for st, s in g2.groupby("structure"):
        m = s.groupby("chunker").delivery.apply(lambda x: (x == "full").mean())
        out.append({"stat": f"gap Cstar-C ({st})", "value": m.get("Cstar", np.nan) - m.get("C", np.nan), "lo": None, "hi": None})
    gs = pd.DataFrame(out).round(3)
    gs.to_csv("results/grid_stats.csv", index=False)
    print("\nGrid (L2 proactive full delivery):")
    print(gs.to_string(index=False))


def sanity(m, sl):
    print("\nSanity:")
    get = lambda c, k: m.loc[m.condition == c, k].iloc[0] if (m.condition == c).any() and k in m else None
    s0x = sl[(sl.condition == "S0") & (sl.slice == "bucket") & (sl.value == "cross") & (sl.subset == "all")]
    if len(s0x):
        print(f"  S0 capture on cross plants: {s0x.L3_loose.iloc[0]:.2f} (want ~0)")
    if "L3_loose" in m:
        top = m.sort_values("L3_loose", ascending=False).iloc[0]
        print(f"  highest L3_loose: {top.condition} {top.L3_loose:.2f} (want OR at or near the top; OR = {get('OR', 'L3_loose')})")
    for a, b in (("Cs2", "C2"),):
        if get(a, "L3_loose") is not None and get(b, "L3_loose") is not None:
            print(f"  {a} {get(a, 'L3_loose'):.2f} vs {b} {get(b, 'L3_loose'):.2f} (want Cstar >= C)")


if __name__ == "__main__":
    main()
