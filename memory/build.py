"""One entry point for every chunker: build_chunks(ws, name) -> list[Chunk].

Names: A, B, C (inferred parents), Cstar (gold parents), D (topic segments), E (rewrite),
Z (zero-call segments, memory.zseg), L (D + labels, memory.label_units).
C, D and E read their LLM output from data/cache (run memory.linker / segment / rewrite first).
"""
from __future__ import annotations

from memory.base import load_msgs
from memory.chunkers import chunk_A, chunk_B, chunk_C, gold_parents
from memory.linker import load_parents
from memory.rewrite import chunk_E, load_rewrite
from memory.segment import chunk_D, load_segments

CHUNKERS = ["A", "B", "C", "Cstar", "D", "E"]   # the original grid; "Z" is built on request only


def build_chunks(ws: str, name: str, msgs: list[dict] | None = None):
    msgs = msgs or load_msgs(ws)
    if name == "A":
        return chunk_A(msgs)
    if name == "B":
        return chunk_B(msgs)
    if name == "Cstar":
        return chunk_C(msgs, gold_parents(msgs))
    if name == "L":                                   # D chunks + LLM labels (memory.label_units)
        from memory.label_units import chunk_L, load_labels
        labels = load_labels(ws)
        if labels is None:
            raise SystemExit(f"no cached labels for {ws}: run python -m memory.label_units --ws {ws}")
        return chunk_L(build_chunks(ws, "D", msgs), labels)
    if name == "Z":                                   # zero-call segmentation (memory.zseg)
        from memory.zseg import chunk_Z
        return chunk_Z(msgs, ws)
    need = {"C": ("linker", load_parents), "D": ("segment", load_segments), "E": ("rewrite", load_rewrite)}
    mod, loader = need[name]
    data = loader(ws)
    if data is None:
        raise SystemExit(f"no cached {mod} output for {ws}: run python -m memory.{mod} --ws {ws}")
    return {"C": lambda: chunk_C(msgs, data), "D": lambda: chunk_D(msgs, data),
            "E": lambda: chunk_E(msgs, data)}[name]()
