"""Shared memory primitives: Chunk, causal visibility, the recent-message window, delivery.

Design: each chunker builds chunks over the WHOLE workspace once. At query time, visible() hides
the future: chunks that end before the query are kept whole, chunks that straddle it are cut back
to their earlier messages (atomic chunks, i.e. E statements, are dropped instead). One build per
chunker instead of one per decision point.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

WS_DIR = Path("data/workspaces")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_msgs: tuple[str, ...]   # msg_ids, in seq order
    first: int                     # seq of earliest source
    last: int                      # seq of latest source
    text: str                      # what gets indexed and shown
    atomic: bool = False           # E statements can't be truncated


def load_msgs(ws: str) -> list[dict]:
    return [json.loads(l) for l in (WS_DIR / ws / "messages.jsonl").read_text().splitlines()]


def load_plants(ws: str, audit: bool = True) -> list[dict]:
    """Plants, with hidden restatements from world/restatement_audit.py merged in as extra
    evidence groups (form 'restatement', origin False). Only hits a human marked verdict='accept'
    are merged; unreviewed hits are ignored. audit=False gives the raw plants."""
    plants = [json.loads(l) for l in (WS_DIR / ws / "plants.jsonl").read_text().splitlines()]
    path = WS_DIR / ws / "restatements.json"
    if audit and path.exists():
        hits = json.loads(path.read_text())
        for p in plants:
            extra = [h for h in hits.get(p["plant_id"]) or [] if h.get("verdict") == "accept"]
            if extra:
                p["evidence_groups"] = p["evidence_groups"] + [
                    {"group": f"{p['plant_id']}@restate/{h['msg_id']}", "form": "restatement",
                     "origin": False, "msgs": [h["msg_id"]], "source": "audit"} for h in extra]
                p["evidence_msgs"] = sorted(set(p.get("evidence_msgs", [])) | {h["msg_id"] for h in extra})
                p["restated"] = True
                p["restated_hidden"] = True
    return plants


def line(m: dict) -> str:
    if m["kind"] == "reaction":
        return f"[{m['day']} {m['channel']}] ({m['speaker']} reacted {m['text']})"
    return f"[{m['day']} {m['channel']}] {m['speaker']}: {m['text']}"


def make_chunk(cid: str, ms: list[dict], prefix: str = "") -> Chunk:
    ms = sorted(ms, key=lambda m: m["seq"])
    return Chunk(cid, tuple(m["msg_id"] for m in ms), ms[0]["seq"], ms[-1]["seq"],
                 prefix + "\n".join(line(m) for m in ms))


def visible(chunks: list[Chunk], q_seq: int, by_id: dict) -> list[Chunk]:
    """What memory may contain when deciding right after message q_seq: only messages before it.

    The query message itself is excluded (it's in the window); everything at or after it is future.
    """
    out = []
    for c in chunks:
        if c.last < q_seq:
            out.append(c)
        elif c.first < q_seq and not c.atomic:
            ms = [by_id[i] for i in c.source_msgs if by_id[i]["seq"] < q_seq]
            out.append(make_chunk(c.chunk_id + "~", ms))
    return out


def window(msgs: list[dict], q_seq: int, channel: str, n: int = 15) -> list[dict]:
    """The last n messages of the channel, up to and including the query message."""
    return [m for m in msgs if m["channel"] == channel and m["seq"] <= q_seq][-n:]


def delivery(retrieved: list[Chunk], window_ids, groups: list[dict]) -> str:
    """full if any evidence group is fully present, partial if any piece is, else none."""
    got = set(window_ids).union(*(c.source_msgs for c in retrieved))
    states = ["full" if set(g["msgs"]) <= got else "partial" if set(g["msgs"]) & got else "none"
              for g in groups]
    return "full" if "full" in states else "partial" if "partial" in states else "none"


def deliveries(retrieved: list[Chunk], window_ids, plant: dict) -> dict:
    """Delivery two ways: against all evidence groups (the real question) and the origin group
    only (the per-form question: did THIS evidence form get through?)."""
    groups = plant.get("evidence_groups") or []
    origin = [g for g in groups if g.get("origin")]
    return {"all": delivery(retrieved, window_ids, groups) if groups else "n/a",
            "origin": delivery(retrieved, window_ids, origin) if origin else "n/a"}


def fact_plants(plants: list[dict]) -> list[dict]:
    """Plants whose decision depends on remembered evidence (have evidence groups)."""
    return [p for p in plants if p.get("kind") == "plant" and p.get("evidence_groups")]
