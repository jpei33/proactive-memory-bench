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
_model_lock = threading.Lock()     # local models (MiniLM, reranker): load once, run one call at a time


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


def _env():
    """Load .env once before the first local-model load (HF_TOKEN for Hugging Face downloads)."""
    if not _local.get("_env"):
        from dotenv import load_dotenv
        load_dotenv(".env")
        _local["_env"] = True


def _key(text: str, kind: str) -> str:
    return hashlib.sha1(f"{kind}|{text}".encode()).hexdigest()


def _compute(texts: list[str], kind: str, model: str | None = None) -> list[np.ndarray]:
    m = model or _model()
    if m.startswith("local:"):
        from sentence_transformers import SentenceTransformer
        name = m.split(":", 1)[1]
        pfx = "Represent this sentence for searching relevant passages: " if kind == "q" and "bge" in name else ""
        with _model_lock:                          # torch models are not safe to load/run from many threads
            _env()
            if name not in _local:
                _local[name] = SentenceTransformer(name)
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


def embed(texts: list[str], kind: str = "d", model: str | None = None) -> list[np.ndarray]:
    """kind: 'd' for documents (chunks), 'q' for queries. model: override EMBED_MODEL."""
    m = model or _model()
    with _lock:
        st = _stores.setdefault(m, _Store(m))
        keys = [_key(t, kind) for t in texts]
        todo = list(dict.fromkeys(t for t, k in zip(texts, keys) if k not in st.vec))
    if todo:
        vecs = _compute(todo, kind, m)
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


# ---------- Threader-style ranker (arm 1 of the 3-way comparison) ----------
# Threader (arXiv 2609.33226): raw topic segments, multi-view dense + BM25 candidates, then
# "localized evidence matching" (mean of the top-K2 message-level cosines), + beta*BM25, optional
# bge cross-encoder fused with weight alpha. Hyperparameters fixed BEFORE any evaluation (the
# paper's values are in its appendix F.6, not used): K1=20, K2=3, views (full, human, agent) =
# (0.5, 0.25, 0.25), beta=0.3, alpha=0.5. Views: human/agent come from the message field
# "is_agent" (real data only); when a view is empty, or no message has the field (simulated data),
# its weight is dropped and the rest renormalized, i.e. simulated data uses the full view only.
# Atomic chunks (E statements) have no raw messages: their only evidence unit is their own text.
# Local models, no API calls: MiniLM embeddings (disk-cached like every vector here); reranker
# scores disk-cached in data/cache/rerank_<model>.json.
THR_EMB = "local:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
THR_RERANK = "BAAI/bge-reranker-base"
THR = {"K1": 20, "K2": 3, "w": (0.5, 0.25, 0.25), "beta": 0.3, "alpha": 0.5, "gamma": 0.15}
# gamma: arm-2 label boost, added to the final score of a candidate whose labels (memory.label_units)
# match the query type. Chunks without labels (D, Z, E, truncated L) are unaffected.


def _msg_index(ws: str) -> dict:
    if ws not in _msg_cache:
        from memory.base import load_msgs
        _msg_cache[ws] = {m["msg_id"]: m for m in load_msgs(ws)}
    return _msg_cache[ws]


_msg_cache: dict[str, dict] = {}


def _views_units(c):
    """-> ([(weight, text)] views, [unit texts]) for one chunk."""
    from memory.base import line
    if c.atomic or not c.source_msgs:
        return [(1.0, c.text)], [c.text]
    idx = _msg_index(c.source_msgs[0].split("/")[0])
    ms = [idx[i] for i in c.source_msgs if i in idx]
    views = [(THR["w"][0], c.text)]                    # full view = what is indexed (incl. labels/headers)
    if any("is_agent" in m for m in ms):
        hum = "\n".join(line(m) for m in ms if not m.get("is_agent"))
        agt = "\n".join(line(m) for m in ms if m.get("is_agent"))
        views += [(w, t) for w, t in ((THR["w"][1], hum), (THR["w"][2], agt)) if t]
    tot = sum(w for w, _ in views)
    return [(w / tot, t) for w, t in views], [line(m) for m in ms] or [c.text]


def _bm25_scores(chunks, q: str) -> np.ndarray:
    return np.asarray(BM25Okapi([tokenize(c.text) or ["_"] for c in chunks]).get_scores(tokenize(q)))


def _minmax(x: np.ndarray) -> np.ndarray:
    lo, hi = float(np.min(x)), float(np.max(x))
    return (x - lo) / (hi - lo) if hi > lo else np.zeros_like(x)


class _RerankCache:
    def __init__(self, model):
        import json as _json
        self.path = Path(f"data/cache/rerank_{model.replace('/', '-')}.json")
        self.s = _json.loads(self.path.read_text()) if self.path.exists() else {}
        self.model, self.ce, self.new = model, None, 0

    def scores(self, q: str, texts: list[str]) -> np.ndarray:
        import json as _json
        keys = [hashlib.sha1(f"{q}\x00{t}".encode()).hexdigest() for t in texts]
        todo = [(k, t) for k, t in zip(keys, texts) if k not in self.s]
        if todo:
            with _model_lock:
                if self.ce is None:
                    from sentence_transformers import CrossEncoder
                    _env()
                    self.ce = CrossEncoder(self.model)
                out = self.ce.predict([(q, t) for _, t in todo])
            with _lock:
                for (k, _), v in zip(todo, out):
                    self.s[k] = float(v)
                self.new += len(todo)
                if self.new >= 200:
                    self.save()
        return np.asarray([self.s[k] for k in keys])

    def save(self):
        import json as _json
        if self.new:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(_json.dumps(self.s))
            self.new = 0


_rr: dict[str, _RerankCache] = {}


def rank_threader(chunks, q: str, rerank: bool = False, boost: bool = True) -> list[int]:
    if not chunks:
        return []
    qv = embed([q], "q", THR_EMB)[0]
    vu = [_views_units(c) for c in chunks]
    allt = list(dict.fromkeys([t for v, u in vu for _, t in v] + [t for _, u in vu for t in u]))
    E = dict(zip(allt, embed(allt, "d", THR_EMB)))
    dense = np.asarray([sum(w * float(E[t] @ qv) for w, t in v) for v, _ in vu])
    bm = _bm25_scores(chunks, q)
    k1 = THR["K1"]
    cand = list(dict.fromkeys(list(np.argsort(-dense)[:k1]) + list(np.argsort(-bm)[:k1])))
    local = np.asarray([np.mean(sorted((float(E[t] @ qv) for t in vu[i][1]), reverse=True)[:THR["K2"]])
                        for i in cand])
    s = _minmax(local) + THR["beta"] * _minmax(bm[cand])
    if rerank:
        rr = _rr.setdefault(THR_RERANK, _RerankCache(THR_RERANK))
        s = (1 - THR["alpha"]) * _minmax(s) + THR["alpha"] * _minmax(rr.scores(q, [chunks[i].text for i in cand]))
    if boost:
        from memory.label_units import chunk_labels, query_types
        qt = query_types(q)
        if qt:
            s = s + THR["gamma"] * np.asarray([bool(qt & set(chunk_labels(chunks[i]))) for i in cand], float)
    head = [cand[j] for j in np.argsort(-s, kind="stable")]
    rest = [int(i) for i in np.argsort(-dense, kind="stable") if i not in set(cand)]
    return [int(i) for i in head] + rest


def rank_threader_rr(chunks, q: str) -> list[int]:
    return rank_threader(chunks, q, rerank=True)


def rank_threader_nob(chunks, q: str) -> list[int]:
    return rank_threader(chunks, q, boost=False)


def save_caches():
    """Flush the reranker cache (embedding stores save themselves)."""
    for r in _rr.values():
        r.save()


RANKERS = {"bm25": rank_bm25, "emb": rank_emb, "rrf": rank_rrf}        # the original 15-cell grid
EXTRA_RANKERS = {"thr": rank_threader, "thr_rr": rank_threader_rr, "thr_nob": rank_threader_nob}     # 3-way comparison only
ALL_RANKERS = {**RANKERS, **EXTRA_RANKERS}

import atexit                                         # noqa: E402
atexit.register(save_caches)


def retrieve(chunks, q: str, ranker: str, budget: int = 1500):
    """Top chunks until the token budget (≈ chars/4) is used up."""
    if not chunks:
        return []
    out, used = [], 0
    for i in ALL_RANKERS[ranker](chunks, q):
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
