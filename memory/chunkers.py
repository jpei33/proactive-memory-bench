"""Chunkers A (per message), B (sliding window), C (reply-linked) and the Cstar parent map.
D (topic segments) and E (write-time rewrite) come in 3.3.

Every chunker takes the whole workspace's messages (seq order) and returns list[Chunk].
"""
from __future__ import annotations

from collections import defaultdict

from memory.base import Chunk, make_chunk


def chunk_A(msgs: list[dict]) -> list[Chunk]:
    """One chunk per message."""
    return [make_chunk(f"A:{m['msg_id']}", [m]) for m in msgs]


def chunk_B(msgs: list[dict], size: int = 6, stride: int = 3) -> list[Chunk]:
    """Overlapping windows of `size` consecutive messages per channel, every `stride` messages."""
    by_ch = defaultdict(list)
    for m in msgs:
        by_ch[m["channel"]].append(m)
    out = []
    for ch, ms in by_ch.items():
        for s in range(0, max(1, len(ms) - size + stride), stride):
            if ms[s:s + size]:
                out.append(make_chunk(f"B:{ch}:{s}", ms[s:s + size]))
    return out


def chunk_C(msgs: list[dict], parent_of: dict, depth: int = 3) -> list[Chunk]:
    """One chunk per message: [grandparent, parent, message], following parent_of links.

    parent_of: msg_id -> parent msg_id or None (gold_parents for Cstar, linker.infer_parents for C).
    """
    by_id = {m["msg_id"]: m for m in msgs}
    out = []
    for m in msgs:
        chain, p = [m], parent_of.get(m["msg_id"])
        while p and p in by_id and len(chain) < depth and by_id[p] not in chain:
            chain.insert(0, by_id[p])
            p = parent_of.get(p)
        out.append(make_chunk(f"C:{m['msg_id']}", chain))
    return out


def gold_parents(msgs: list[dict]) -> dict:
    """Cstar: the simulator's true reply links (an upper bound no real system has)."""
    return {m["msg_id"]: m["reply_to"] for m in msgs}
