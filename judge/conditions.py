"""Memory conditions for the judge: what goes in the MEMORY slot at one decision point.

Names
  S0                no memory (recent window only)
  OR                oracle: the team-facts box human labelers saw (perfect memory of facts/open items)
  <chunker><r>      retrieval cell. chunker in A B C D E, or Cs for Cstar; r = 1 bm25, 2 emb, 3 rrf
                    e.g. A1 = per-message + BM25, E3 = rewrite + RRF, Cs2 = gold reply links + embeddings
Proactive query = the last 3 window messages (the decision message is the last).
Chunks are visible(all chunks, seq) minus chunks whose sources are all in the window.
"""
from __future__ import annotations

from functools import lru_cache

from label.context import recent, team_facts, today
from memory.base import deliveries, load_msgs, load_plants, visible, window
from memory.build import build_chunks
from memory.retrievers import retrieve
from sim.run_workspace import load

RET = {"1": "bm25", "2": "emb", "3": "rrf", "4": "thr", "5": "thr_rr", "6": "thr_nob"}  # 4/5/6: Threader (5 = + reranker, 6 = no label boost)
CHUNK = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "Cs": "Cstar", "Z": "Z", "L": "L"}
GRID = [f"{c}{r}" for c in "ABCDE" for r in "123"]


def base_of(cond: str) -> str:
    """'E1+OI~haiku' -> 'E1'"""
    return cond.split("~")[0].split("+")[0]


def parse(cond: str):
    cond = base_of(cond)
    if cond in ("S0", "OR"):
        return cond, None
    return CHUNK[cond[:-1]], RET[cond[-1]]


@lru_cache(maxsize=None)
def ws_data(ws):
    msgs = load_msgs(ws)
    return load(ws), msgs, {m["msg_id"]: m for m in msgs}, {p["plant_id"]: p for p in load_plants(ws)}


@lru_cache(maxsize=None)
def chunks(ws, chunker):
    return build_chunks(ws, chunker, ws_data(ws)[1])


def query_text(ws, seq, channel):
    _, msgs, _, _ = ws_data(ws)
    return " \n".join(m["text"] for m in window(msgs, seq, channel)[-3:])


def point_view(point):
    """(window msg ids, window text, proactive query, today) for a decision point.

    A virtual point (probe conflict/control) carries {"virtual": {"speaker", "text"}}: its message is
    not in the chat. It sits just before message `seq`, so the window is the 14 channel messages before
    seq plus the virtual message, and memory sees seq < `seq`.
    """
    ws, seq, ch = point["ws"], point["seq"], point["channel"]
    _, msgs, _, _ = ws_data(ws)
    v = point.get("virtual")
    if not v:
        return ([m["msg_id"] for m in window(msgs, seq, ch)], recent(msgs, seq, ch),
                query_text(ws, seq, ch), today(msgs, seq))
    prev = window(msgs, seq - 1, ch, n=14)
    day = today(msgs, seq)
    text = recent(msgs, seq - 1, ch, n=14) if prev else ""
    if not prev or prev[-1]["day"] != day:
        text += ("\n" if text else "") + f"--- {day} · {ch} ---"
    text += f"\n{v['speaker']}: {v['text']}"
    q = " \n".join([m["text"] for m in prev[-2:]] + [v["text"]])
    return [m["msg_id"] for m in prev], text, q, day


def visible_chunks(ws, chunker, seq, channel, win_ids=None):
    _, msgs, by_id, _ = ws_data(ws)
    win = set(win_ids) if win_ids is not None else {m["msg_id"] for m in window(msgs, seq, channel)}
    return [c for c in visible(chunks(ws, chunker), seq, by_id) if not set(c.source_msgs) <= win]


def build(point: dict, cond: str, budget: int = 1500) -> dict:
    """-> {today, channel, window, memory, retrieved, delivery}"""
    ws, seq, ch = point["ws"], point["seq"], point["channel"]
    d, msgs, by_id, plants = ws_data(ws)
    win_ids, win_text, qtext, day = point_view(point)
    chunker, ret = parse(cond)
    retrieved, memory, got = [], "", []
    b = base_of(cond)
    if b == "OR":
        memory = team_facts(d, msgs, seq)
    elif b != "S0":
        got = retrieve(visible_chunks(ws, chunker, seq, ch, win_ids), qtext, ret, budget)
        retrieved = [c.chunk_id for c in got]
        memory = "\n---\n".join(c.text for c in got)
    if "+OI" in cond:                     # oracle open-item tracker: ledger open items with check points
        items = [l for l in team_facts(d, msgs, seq).splitlines() if l.startswith("- open item:")]
        memory += "\n\nOPEN ITEMS (commitments and pending decisions not yet resolved):\n" + ("\n".join(items) or "(none)")
    if "+T" in cond:                      # the agent's own tracker: what it TRACKed earlier in its E1 run
        memory += "\n\nYOUR TRACKED ITEMS (you chose TRACK on these earlier):\n" + (own_tracks(ws, seq) or "(none)")
    p = point if point.get("evidence_groups") else plants.get(point.get("plant_id") or "")
    if p and p.get("evidence_groups") and b != "OR":
        dl = deliveries(got, win_ids, p)["all"]
    else:
        dl = "n/a"
    return {"today": day, "channel": ch, "window": win_text,
            "memory": memory, "retrieved": retrieved, "delivery": dl}


@lru_cache(maxsize=None)
def _tracks():
    import json
    from pathlib import Path
    pts = {p["point_id"]: p for p in json.load(open("data/eval_points.json"))}
    out = []
    path = Path("data/runs/E1_b1500.jsonl")
    for l in (path.open() if path.exists() else []):
        r = json.loads(l)
        if r["label"] == "TRACK" and r["point_id"] in pts:
            pt = pts[r["point_id"]]
            out.append((pt["ws"], pt["seq"], r["cited_value"] or r["reason"]))
    return out


def own_tracks(ws, seq):
    d, msgs, _, _ = ws_data(ws)
    day = {m["seq"]: m["day"] for m in msgs}
    return "\n".join(f"- tracked {day[s]}: {t}" for w, s, t in sorted(_tracks(), key=lambda x: x[1]) if w == ws and s < seq)


def prefetch_all(points, conds):
    """Embed every visible chunk text and query the run will need, in one batched pass per ws."""
    from memory.retrievers import prefetch
    for ws in sorted({p["ws"] for p in points}):
        pts = [p for p in points if p["ws"] == ws]
        need = {parse(c)[0] for c in conds if parse(c)[1] in ("emb", "rrf")}
        views = {id(p): point_view(p) for p in pts}
        texts = {c.text for ck in need for p in pts
                 for c in visible_chunks(ws, ck, p["seq"], p["channel"], views[id(p)][0])}
        prefetch(list(texts), "d")
        prefetch([views[id(p)][2] for p in pts], "q")
