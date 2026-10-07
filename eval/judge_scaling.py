"""Memory gap vs judge strength on the paired conflict/control probes.

    python -m eval.judge_scaling

Judges: Sonnet = untagged runs, plus every ~tag in data/runs/probes (gpt, haiku, opus, ...).

  strength  = mean balanced accuracy of the judge over the real-memory conditions NOT used in any
              gap (A3, Cs2, D2), so x and the plotted gaps come from different judge calls.
              (Oracle bal-acc was used first but is a poor strength measure: oracle memory makes
              judges over-intervene, and E1 beats OR on bal-acc for GPT and Opus.)
  gaps      = within-judge paired differences in BALANCED ACCURACY ((catch + 1 - false_alarm) / 2)
              between memory conditions. Catch rate alone rewards trigger-happy judges (Haiku
              catches 68% under B3 but false-alarms on 46% of controls), so bal-acc is the headline;
              catch-rate gaps are written to the csv too.
  delivery  = catch|full, catch|not_full pooled over A3+B3 (the real-memory conditions every judge
              has), plus false-alarm rate on those conditions' controls.
A gap is reported only if the judge has a complete run (all probes) for both conditions.
CIs: 95% bootstrap over facts (conflict + control probes sharing a fact resampled together).
Writes results/judge_scaling.csv and results/figs/judge_scaling.png
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

DIR = Path("data/runs/probes")
POINTS = Path("data/probe_points.json")
B = 2000
RNG = np.random.default_rng(0)
POOL = ["A3", "B3"]
STRENGTH = ["A3", "Cs2", "D2"]
GAPS = [("B3", "S0"), ("A3", "S0"), ("E1", "S0"), ("E1", "B3"), ("OR", "B3")]
NAMES = {"": "Sonnet 5.5", "gpt": "GPT-6 Luna", "haiku": "Haiku 4.5", "opus": "Opus 5.5"}


def load():
    pts = {p["point_id"]: p for p in json.load(open(POINTS))}
    rows = []
    for f in sorted(DIR.glob("*_b*.jsonl")):
        for l in f.open():
            r = json.loads(l)
            p = pts.get(r["point_id"])
            if not p or r["label"] == "INVALID":
                continue
            base, _, tag = r["condition"].partition("~")
            rows.append({"base": base, "judge": tag, "fact": f"{p['ws']}:{p['fact_id']}",
                         "kind": p["kind"], "iv": float(r["label"] == "INTERVENE"),
                         "full": r["delivery"] == "full"})
    return pd.DataFrame(rows), len(pts)


def stats(d):
    """All per-judge quantities on one (possibly resampled) frame -> dict."""
    g = d.groupby(["base", "kind"]).iv.mean()
    out = {}
    def bal(c):
        try:
            return (g[(c, "probe_conflict")] + 1 - g[(c, "probe_control")]) / 2
        except KeyError:
            return np.nan
    def catch(c):
        return g.get((c, "probe_conflict"), np.nan)
    out["strength"] = np.nanmean([bal(c) for c in STRENGTH])
    for a, b in GAPS:
        out[f"bal_{a}_{b}"] = bal(a) - bal(b)
        out[f"catch_{a}_{b}"] = catch(a) - catch(b)
    pool = d[d.base.isin(POOL)]
    conf, ctrl = pool[pool.kind == "probe_conflict"], pool[pool.kind == "probe_control"]
    out["catch_full"] = conf[conf.full].iv.mean()
    out["catch_not_full"] = conf[~conf.full].iv.mean()
    out["false_alarm"] = ctrl.iv.mean()
    return out


def main():
    df, n_pts = load()
    out = []
    for j in df.judge.unique():
        d = df[df.judge == j]
        n = d.groupby("base").size()
        complete = set(n[n == n_pts].index)
        d = d[d.base.isin(complete)]
        if not {"OR", "B3", "S0"} <= complete:
            continue
        facts = d.fact.unique()
        groups = {f: g for f, g in d.groupby("fact")}
        obs = stats(d)
        bs = pd.DataFrame([stats(pd.concat([groups[f] for f in RNG.choice(facts, len(facts))]))
                           for _ in range(B)])
        row = {"judge": NAMES.get(j, j), "tag": j or "sonnet", "conditions": ",".join(sorted(complete))}
        for k, v in obs.items():
            lo, hi = np.nanpercentile(bs[k], [2.5, 97.5]) if not np.isnan(v) else (np.nan, np.nan)
            row[k], row[k + "_lo"], row[k + "_hi"] = 100 * v, 100 * lo, 100 * hi
        out.append(row)
    res = pd.DataFrame(out).sort_values("strength").reset_index(drop=True)
    Path("results/figs").mkdir(parents=True, exist_ok=True)
    res.round(1).to_csv("results/judge_scaling.csv", index=False)

    def fmt(k):
        return [("   n/a" if np.isnan(v) else f"{v:+5.1f} [{l:+.0f},{h:+.0f}]")
                for v, l, h in zip(res[k], res[k + "_lo"], res[k + "_hi"])]
    show = pd.DataFrame({"judge": res.judge, "strength": res.strength.round(1)})
    for a, b in GAPS:
        show[f"bal {a}-{b}"] = fmt(f"bal_{a}_{b}")
    print(show.to_string(index=False))
    show2 = res[["judge", "catch_full", "catch_not_full", "false_alarm"]].round(1)
    for a, b in [("E1", "B3"), ("B3", "S0")]:
        show2[f"catch {a}-{b}"] = res[f"catch_{a}_{b}"].round(1)
    print("\n" + show2.to_string(index=False))
    plot(res)


def plot(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    blue, orange, aqua = "#2a78d6", "#eb6834", "#1baf7a"
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": grid, "axes.labelcolor": ink2,
                         "xtick.color": ink2, "ytick.color": ink2, "axes.titlecolor": ink,
                         "figure.facecolor": surf, "axes.facecolor": surf})
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    x = res.strength.values
    xerr = [x - res.strength_lo, res.strength_hi - x]

    def series(ax, key, color, label, hollow=False, fit=True, dx=0.0):
        m = ~res[key].isna()
        if not m.any():
            return
        xs, y = x[m] + dx, res[key].values[m]
        ax.errorbar(xs, y, xerr=[xerr[0][m], xerr[1][m]], fmt="none", ecolor=color, elinewidth=1,
                    alpha=0.3, zorder=2)
        ax.errorbar(xs, y, yerr=[y - res[key + "_lo"][m], res[key + "_hi"][m] - y],
                    fmt="o", ms=8, color=color, ecolor=color,
                    elinewidth=1.4, capsize=0, mfc=surf if hollow else color, mec=color if hollow else surf,
                    mew=2, label=label, zorder=3)
        if fit and m.sum() >= 3:
            k, c = np.polyfit(xs, y, 1)
            xx = np.linspace(xs.min() - 1, xs.max() + 1, 10)
            ax.plot(xx, k * xx + c, color=color, lw=2, alpha=0.3, zorder=2)

    def style(ax, title, ylabel):
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
        ax.set_ylabel(ylabel)
        ax.set_xlabel("judge strength: mean bal. accuracy on A3/Cs2/D2 memory (%)")
        ax.grid(True, color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    a0, a1, a2 = axes
    series(a0, "bal_B3_S0", blue, "B3 − S0 (all judges)")
    series(a0, "bal_E1_S0", orange, "E1 − S0", dx=0.25)
    style(a0, "Memory vs. no memory", "balanced-accuracy gap (pts)")
    a0.axhline(0, color=ink2, lw=1)
    def names(ax, key, dx=0.0):
        for xi, yi, name in zip(x, res[key], res.judge):
            if np.isnan(yi):
                continue
            off, ha = OFFS.get(name, ((-8, 8), "right"))
            ax.annotate(name, (xi + dx, yi), xytext=off, textcoords="offset points", color=ink,
                        fontsize=9, ha=ha)
    OFFS = {"Opus 5.5": ((10, -14), "left"), "GPT-6 Luna": ((8, -16), "left"),
            "Haiku 4.5": ((10, -4), "left"), "Sonnet 5.5": ((10, -4), "left")}
    names(a0, "bal_B3_S0")
    a0.legend(frameon=False, loc="upper left", fontsize=9, labelcolor=ink2)

    series(a1, "bal_E1_B3", orange, "E1 − B3")
    series(a1, "bal_OR_B3", blue, "Oracle − B3", hollow=True, dx=0.25)
    style(a1, "Better vs. worse memory", "balanced-accuracy gap (pts)")
    names(a1, "bal_OR_B3", 0.25)
    a1.axhline(0, color=ink2, lw=1)
    a1.legend(frameon=False, loc="upper left", fontsize=9, labelcolor=ink2)

    series(a2, "catch_full", aqua, "catch | full fact delivered")
    series(a2, "catch_not_full", orange, "catch | partial or none")
    series(a2, "false_alarm", blue, "false alarm on controls", hollow=True)
    style(a2, "What the judge does with A3/B3 memory", "rate (%)")
    a2.legend(frameon=False, loc="center right", fontsize=9, labelcolor=ink2)

    fig.suptitle("Memory gap vs. judge strength  (probe set, within-judge paired gaps, 95% CIs over facts)",
                 x=0.01, ha="left", fontsize=12, color=ink)
    fig.text(0.01, 0.005, "Judge strength (x): " + " < ".join(res.judge) + ".  "
             "Faint horizontal bars = CI on x.",
             fontsize=8.5, color=ink2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig("results/figs/judge_scaling.png", dpi=180)
    print("\n-> results/judge_scaling.csv, results/figs/judge_scaling.png")


if __name__ == "__main__":
    main()
