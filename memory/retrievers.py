"""Retrievers over chunks: BM25 (lexical, grep-like), embeddings (semantic), hybrid RRF.

Embedding model (set in .env):
    EMBED_MODEL=text-embedding-3-large        # default; OpenAI API, uses OPENAI_API_KEY
    EMBED_MODEL=local:BAAI/bge-small-en-v1.5  # free local alternative (uv add sentence-transformers)
Every vector is cached on disk (data/cache/emb_<model>.npz), so each text is embedded once ever.

    python -m memory.retrievers --ws ando --plant ando-p16 --chunker A    # 3.4 check
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import threading
from collections import defaultdict
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

TOK = re.compile(r"[a-z0-9$%@]+(?:[-_.,][a-z0-9]+)*")


def tokenize(s: str) -> list[str]:
    toks = TOK.findall(s.lower())
    return toks + [p for t in toks if "-" in t for p in t.split("-")]   # and-341 -> and-341, and, 341


# ---------- embeddings ----------
DIM = 1024                                   # text-embedding-3-large truncated (Matryoshka); plenty here
_lock = threading.Lock()


def _model() -> str:
    return os.environ.get("EMBED_MODEL", "text-embedding-3-large")


class _Store:
    def __init__(self, model):
        self.path = Path(f"data/cache/emb_{model.replace('/', '-').replace(':', '-')}.npz")
        self.vec = dict(np.load(self.path)) if self.path.exists() else {}
        self.dirty = False

    def save(self):
        if self.dirty:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(self.path, **self.vec)
            self.dirty = False


_stores: dict[str, _Store] = {}
_local = {}


def _key(text: str, kind: str) -> str:
    return hashlib.sha1(f"{kind}|{text}".encode()).hexdigest()


def _compute(texts: list[str], kind: str) -> list[np.ndarray]:
    m = _model()
    if m.startswith("local:"):
        from sentence_transformers import SentenceTransformer
        name = m.split(":", 1)[1]
        if name not in _local:
            _local[name] = SentenceTransformer(name)
        pfx = "Represent this sentence for searching relevant passages: " if kind == "q" and "bge" in name else ""
        return list(_local[name].encode([pfx + t for t in texts], normalize_embeddings=True, batch_size=64))
    from openai import OpenAI
    client, out = OpenAI(), []
    for i in range(0, len(texts), 256):
        batch = [t if t.strip() else "(empty)" for t in texts[i:i + 256]]
        r = client.embeddings.create(model=m, input=batch, dimensions=DIM)
        for d in r.data:
            v = np.asarray(d.embedding, dtype=np.float32)
            out.append(v / np.linalg.norm(v))
    return out


def embed(texts: list[str], kind: str = "d") -> list[np.ndarray]:
    """kind: 'd' for documents (chunks), 'q' for queries."""
    m = _model()
    with _lock:
        st = _stores.setdefault(m, _Store(m))
        keys = [_key(t, kind) for t in texts]
        todo = list(dict.fromkeys(t for t, k in zip(texts, keys) if k not in st.vec))
    if todo:
        vecs = _compute(todo, kind)
        with _lock:
            for t, v in zip(todo, vecs):
                st.vec[_key(t, kind)] = v
            st.dirty = True
            st.save()
    return [st.vec[k] for k in keys]


def prefetch(texts: list[str], kind: str = "d"):
    """Embed many texts up front (one batched pass) so ranking calls never hit the API."""
    embed(texts, kind)


# ---------- rankers: return chunk indices, best first ----------
def rank_bm25(chunks, q: str) -> list[int]:
    s = BM25Okapi([tokenize(c.text) or ["_"] for c in chunks]).get_scores(tokenize(q))
    return sorted(range(len(chunks)), key=lambda i: -s[i])


def rank_emb(chunks, q: str) -> list[int]:
    qv = embed([q], "q")[0]
    s = [float(v @ qv) for v in embed([c.text for c in chunks], "d")]
    return sorted(range(len(chunks)), key=lambda i: -s[i])


def rank_rrf(chunks, q: str, k: int = 60) -> list[int]:
    score = defaultdict(float)
    for ranking in (rank_bm25(chunks, q), rank_emb(chunks, q)):
        for r, i in enumerate(ranking):
            score[i] += 1 / (k + r + 1)
    return sorted(score, key=score.get, reverse=True)


RANKERS = {"bm25": rank_bm25, "emb": rank_emb, "rrf": rank_rrf}


def retrieve(chunks, q: str, ranker: str, budget: int = 1500):
    """Top chunks until the token budget (≈ chars/4) is used up."""
    if not chunks:
        return []
    out, used = [], 0
    for i in RANKERS[ranker](chunks, q):
        n = len(chunks[i].text) // 4
        if used + n > budget:
            break
        out.append(chunks[i])
        used += n
    return out


def main():
    from dotenv import load_dotenv
    load_dotenv(".env")
    from memory.base import deliveries, load_msgs, load_plants, visible, window
    from memory.build import build_chunks
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", default="ando")
    ap.add_argument("--plant", default="ando-p16")
    ap.add_argument("--chunker", default="A")
    ap.add_argument("--rankers", default="bm25,emb,rrf")
    a = ap.parse_args()
    msgs = load_msgs(a.ws)
    by_id = {m["msg_id"]: m for m in msgs}
    p = next(x for x in load_plants(a.ws) if x["plant_id"] == a.plant)
    trig = by_id[p["trigger_msg"]]
    chunks = visible(build_chunks(a.ws, a.chunker, msgs), trig["seq"], by_id)
    win = [m["msg_id"] for m in window(msgs, trig["seq"], trig["channel"])]
    ev = [i for g in p["evidence_groups"] for i in g["msgs"]]
    print(f"{a.plant} ({p['type']}, {p.get('bucket')}) query = {trig['speaker']}: {trig['text']}")
    for i in ev:
        print(f"  evidence {i}: {by_id[i]['speaker']}: {by_id[i]['text'][:90]}")
    for r in a.rankers.split(","):
        order = RANKERS[r](chunks, trig["text"])
        pos = {}
        for rank, ci in enumerate(order, 1):
            for mid in chunks[ci].source_msgs:
                pos.setdefault(mid, rank)
        got = retrieve(chunks, trig["text"], r)
        print(f"\n  {r}: rank of each evidence msg among {len(chunks)} chunks: "
              + ", ".join(f"{i.split('/', 1)[1]}={pos.get(i, '-')}" for i in ev)
              + f" | delivery @1500 tok: {deliveries(got, win, p)}")
        for ci in order[:5]:
            print(f"    {chunks[ci].text[:110]!r}".replace("\\n", " / "))


if __name__ == "__main__":
    main()
