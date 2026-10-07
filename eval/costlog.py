"""Cost log for the 3-way memory comparison (Threader-style vs labeled units vs rewrite).

    from eval.costlog import log, log_result, timed

    log(arm="L4", stage="label", ws="ando", model="claude-haiku-4-5-20251001",
        calls=1, in_tok=812, out_tok=20, seconds=1.3, n_items=1)
    log_result(r, arm="L4", stage="label", ws="ando", model=model)   # r = sim.llm Result
    with timed(arm="D4", stage="index", ws="ando", n_items=len(msgs)) as row:
        ...build the index...                                         # seconds filled in on exit

    python -m eval.costlog            # summary per arm x stage (skips arms starting with "_")

One JSON row per event -> results/threeway_cost.jsonl. Dollars are NOT stored: they are computed at
summary time from eval/prices.json, so a price change never needs a rerun.

Cached LLM calls: log them with cached=True and their ORIGINAL token counts. A cache hit costs
nothing on this run but is still part of the arm's write-time cost; summaries count all rows.
If a cached Result has no token counts, pass the counts from when it was first made.

Stages (suggested): segment (shared D segmentation), label (arm 2), rewrite (arm 3), embed / index
(local, $0), retrieve (per query), judge (per decision).
"""
from __future__ import annotations

import json
import time
from contextlib import contextmanager
from pathlib import Path

LOG = Path("results/threeway_cost.jsonl")
PRICES = Path("eval/prices.json")
FIELDS = ("arm", "stage", "ws", "model", "calls", "in_tok", "out_tok", "cache_read_tok",
          "seconds", "n_items", "cached", "note")


def log(arm: str, stage: str, ws: str = "", model: str = "", calls: int = 0, in_tok: int = 0,
        out_tok: int = 0, cache_read_tok: int = 0, seconds: float = 0.0, n_items: int = 1,
        cached: bool = False, note: str = "", path: Path = LOG) -> dict:
    row = {"ts": round(time.time(), 3), "arm": arm, "stage": stage, "ws": ws, "model": model,
           "calls": int(calls), "in_tok": int(in_tok or 0), "out_tok": int(out_tok or 0),
           "cache_read_tok": int(cache_read_tok or 0), "seconds": round(float(seconds or 0), 4),
           "n_items": int(n_items), "cached": bool(cached), "note": note}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(row) + "\n")
    return row


def log_result(r, arm: str, stage: str, ws: str = "", model: str = "", n_items: int = 1,
               note: str = "") -> dict:
    """Log one sim.llm Result (fields: in_tok, out_tok, cache_read_tok, latency_s, cached)."""
    return log(arm, stage, ws, model, calls=1, in_tok=getattr(r, "in_tok", 0) or 0,
               out_tok=getattr(r, "out_tok", 0) or 0,
               cache_read_tok=getattr(r, "cache_read_tok", 0) or 0,
               seconds=getattr(r, "latency_s", 0) or 0, n_items=n_items,
               cached=bool(getattr(r, "cached", False)), note=note)


@contextmanager
def timed(arm: str, stage: str, ws: str = "", n_items: int = 1, **kw):
    """Time a local (no-LLM) step; mutate the yielded dict to add calls/tokens before exit."""
    row = {"calls": 0, **kw}
    t0 = time.perf_counter()
    try:
        yield row
    finally:
        log(arm, stage, ws, seconds=time.perf_counter() - t0, n_items=n_items, **row)


def price(row: dict, prices: dict | None = None) -> float:
    """USD for one row. Model ids match prices.json keys by prefix (dated ids are fine)."""
    if not row.get("model") or not row.get("calls"):
        return 0.0
    prices = prices or json.load(open(PRICES))
    key = next((k for k in prices if not k.startswith("_") and row["model"].startswith(k)), None)
    if key is None:
        raise KeyError(f"no price for model {row['model']!r} in {PRICES}")
    p = prices[key]
    return (row["in_tok"] * p["in"] + row["out_tok"] * p["out"]
            + row["cache_read_tok"] * p.get("cache_read", p["in"])) / 1e6


def load(path: Path = LOG) -> list[dict]:
    return [json.loads(l) for l in path.open()] if path.exists() else []


def main():
    import pandas as pd
    rows = [r for r in load() if not r["arm"].startswith("_")]
    if not rows:
        print("no rows yet in", LOG)
        return
    prices = json.load(open(PRICES))
    df = pd.DataFrame(rows)
    df["usd"] = [price(r, prices) for r in rows]
    g = df.groupby(["arm", "stage"]).agg(calls=("calls", "sum"), in_tok=("in_tok", "sum"),
                                         out_tok=("out_tok", "sum"), usd=("usd", "sum"),
                                         seconds=("seconds", "sum"), n_items=("n_items", "sum"),
                                         cached_share=("cached", "mean"))
    print(g.round(4).to_string())


if __name__ == "__main__":
    main()
