"""Step 6: does rewrite memory (arm 3, chunker E) keep the facts it was built from?

    python -m eval.fidelity        # -> results/threeway_fidelity.csv + summary (no API calls)

Simulated data (ground truth = the ledger):
  items: the 36 fact plants (gold_value) and the conflict probes' facts (current value), deduped by
         (ws, fact, value). Each item has evidence groups (origin statement, restatements, ...).
  raw_has   the value appears in the evidence messages as raw arms show them (speaker: text)
  kept      some E statement derived from an evidence message (its source_msgs overlap the group)
            contains the value (sim.run_workspace.vpat, the same matcher the probes use)
  kept_ent  ...and also names the fact's entity (ledger keys), i.e. a usable fact, not a stray
            number
  Split of arm 3's misses: write-time loss (not kept) vs retrieval loss (kept, not retrieved).
  Retrieval side uses the existing Sonnet E1 probe runs (data/runs/probes/E1_b1500.jsonl): their
  "delivery" field credits a statement because its SOURCE message is evidence; value_in_memory
  checks the value is actually in the text the judge saw. The gap between the two is delivery
  that the source-message metric over-credits for E.

Real data: share of messages E dropped entirely (0 statements), overall and among the reference
targets of data/real/ref_queries.jsonl. Only counts are written (no message text).
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import pandas as pd

from memory.base import line, load_msgs, load_plants
from memory.rewrite import load_rewrite
from sim.run_workspace import keys_regex, load, vpat

SIM = ["ando", "anthropic", "openai", "xai"]


def statements(ws):
    """msg_id -> [statement texts derived from it (as source or 'uses')]."""
    by_src = defaultdict(list)
    for r in load_rewrite(ws) or []:
        for s in r["statements"]:
            for mid in set(s["uses"]) | {r["msg_id"]}:
                by_src[mid].append(s["text"])
    return by_src


def items():
    out = []
    for ws in SIM:
        for p in load_plants(ws):
            if p.get("kind") == "plant" and p.get("evidence_groups") and p.get("gold_value") and p.get("fact_id"):
                out.append({"src": "plant", "id": p["plant_id"], "ws": ws, "fact": p["fact_id"],
                            "value": p["gold_value"], "groups": p["evidence_groups"]})
    for p in json.load(open("data/probe_points.json")):
        if p["kind"] == "probe_conflict" and p.get("evidence_groups"):
            out.append({"src": "probe", "id": p["point_id"], "ws": p["ws"], "fact": p["fact_id"],
                        "value": p["current"], "groups": p["evidence_groups"]})
    return out


def main():
    rows, st, D, M = [], {}, {}, {}
    for ws in SIM:
        st[ws], D[ws] = statements(ws), load(ws)
        M[ws] = {m["msg_id"]: m for m in load_msgs(ws)}
    seen = set()
    for it in items():
        key = (it["src"], it["ws"], it["fact"], it["value"])
        if key in seen:
            continue
        seen.add(key)
        ws, d = it["ws"], D[it["ws"]]
        vp, kp = vpat(d, it["fact"], it["value"]), keys_regex(d["_fact"][it["fact"]]["keys"])
        origin = [g for g in it["groups"] if g.get("origin")] or it["groups"][:1]
        form = origin[0].get("form", "?")

        def check(groups):
            msgs = [m for g in groups for m in g["msgs"] if m in M[ws]]
            raw = any(vp.search(line(M[ws][m])) for m in msgs)
            ss = [s for m in msgs for s in st[ws].get(m, [])]
            return raw, any(vp.search(s) for s in ss), any(vp.search(s) and kp.search(s) for s in ss), len(ss)
        r_o, k_o, ke_o, n_o = check(origin)
        r_a, k_a, ke_a, _ = check(it["groups"])
        rows.append({"src": it["src"], "ws": ws, "fact": it["fact"], "value": it["value"], "form": form,
                     "raw_has_origin": r_o, "kept_origin": k_o, "kept_ent_origin": ke_o,
                     "stmts_from_origin": n_o, "raw_has_any": r_a, "kept_any": k_a, "kept_ent_any": ke_a})
    df = pd.DataFrame(rows)

    # retrieval side: what the Sonnet E1 probe runs actually handed the judge
    pts = {p["point_id"]: p for p in json.load(open("data/probe_points.json"))}
    ret = []
    for l in open("data/runs/probes/E1_b1500.jsonl"):
        r = json.loads(l)
        p = pts.get(r["point_id"])
        if not p or p["kind"] != "probe_conflict":
            continue
        d = D[p["ws"]]
        ret.append({"ws": p["ws"], "fact": p["fact_id"], "value": p["current"], "form": p["origin_form"],
                    "delivery_full": r["delivery"] == "full",
                    "value_in_memory": bool(vpat(d, p["fact_id"], p["current"]).search(r["memory_text"] or "")),
                    "intervened": r["label"] == "INTERVENE"})
    rt = pd.DataFrame(ret)
    Path("results").mkdir(exist_ok=True)
    df.to_csv("results/threeway_fidelity.csv", index=False)

    pct = lambda s: f"{100 * s.mean():5.1f}%"
    print("== Write-time fidelity of rewrite memory (E), simulated ==")
    for src in ("plant", "probe"):
        s = df[df.src == src]
        print(f"{src}s: {len(s)} facts | value in raw evidence {pct(s.raw_has_origin)} | "
              f"kept by E (origin msgs) {pct(s.kept_origin)} | kept with entity {pct(s.kept_ent_origin)} | "
              f"kept anywhere in evidence {pct(s.kept_any)}")
    print("\nby evidence form (plants + probes, origin group):")
    g = df.groupby("form").agg(n=("form", "size"), raw=("raw_has_origin", "mean"), kept=("kept_origin", "mean"),
                               kept_ent=("kept_ent_origin", "mean"), no_stmt=("stmts_from_origin", lambda x: (x == 0).mean()))
    print((g.assign(**{c: (100 * g[c]).round(0) for c in ["raw", "kept", "kept_ent", "no_stmt"]})).to_string())
    lost_raw = df[df.raw_has_origin & ~df.kept_origin]
    gained = df[~df.raw_has_origin & df.kept_origin]
    print(f"\nE lost a value that WAS in the raw text: {len(lost_raw)}/{df.raw_has_origin.sum()} | "
          f"E surfaced a value NOT literally in raw text (resolved it): {len(gained)}/{(~df.raw_has_origin).sum()}")

    print("\n== Retrieval side: Sonnet E1 probe runs (142 conflict probes) ==")
    print(f"delivery=full (source-message metric) {pct(rt.delivery_full)} | value actually in memory text "
          f"{pct(rt.value_in_memory)} | full but value absent {pct(rt.delivery_full & ~rt.value_in_memory)}")
    for name, sub in [("value in memory", rt[rt.value_in_memory]), ("value NOT in memory", rt[~rt.value_in_memory])]:
        print(f"  catch rate when {name}: {pct(sub.intervened)} (n={len(sub)})")

    # real data
    rw = {r["msg_id"]: len(r["statements"]) for r in load_rewrite("real") or []}
    msgs = load_msgs("real")
    zero = [m for m in msgs if rw.get(m["msg_id"], 0) == 0]
    print("\n== Real data ==")
    print(f"messages with 0 statements: {len(zero)}/{len(msgs)} ({100 * len(zero) / len(msgs):.1f}%)"
          f"  [empty text: {sum(not m['text'] for m in zero)}; agent msgs: {sum(m['is_agent'] for m in zero)}]")
    rq = Path("data/real/ref_queries.jsonl")
    if rq.exists():
        qs = [json.loads(l) for l in rq.open()]
        for kind in sorted({q["kind"] for q in qs}):
            ts = [t for q in qs if q["kind"] == kind for t in q["target_msg_ids"]]
            allz = sum(all(rw.get(t, 0) == 0 for t in q["target_msg_ids"]) for q in qs if q["kind"] == kind)
            print(f"  {kind}: targets dropped by E {sum(rw.get(t, 0) == 0 for t in ts)}/{len(ts)}; "
                  f"queries whose every target was dropped {allz}/{sum(q['kind'] == kind for q in qs)}")
    print("\n-> results/threeway_fidelity.csv")


if __name__ == "__main__":
    main()
