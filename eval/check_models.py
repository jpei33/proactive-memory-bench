"""Step 0 check for the 3-way comparison: do the local models load, and does the cost log write?

    uv run python -m eval.check_models

Downloads on first run (~470 MB MiniLM-L12 multilingual + ~1.1 GB bge-reranker-base) into the
Hugging Face cache. Writes test rows with arm "_test" to results/threeway_cost.jsonl (summaries skip
arms starting with "_"). If the reranker fails, arm 1 runs without it (allowed by the plan).
"""
from __future__ import annotations

import time

from eval.costlog import LOG, log

EMB = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
RERANK = "BAAI/bge-reranker-base"


def main():
    ok = True
    q = "who took the AND-341 migration?"
    docs = ["AJ: I'll take it, should be done by Friday", "lunch at noon anyone?"]

    t0 = time.perf_counter()
    try:
        from sentence_transformers import SentenceTransformer
        m = SentenceTransformer(EMB)
        e = m.encode([q] + docs, normalize_embeddings=True)
        sims = (e[1:] @ e[0]).round(3).tolist()
        dt = time.perf_counter() - t0
        log("_test", "check_embed", model="", seconds=dt, n_items=3, note=EMB)
        print(f"[ok] embedder  {EMB}: dim={e.shape[1]}, cos(q, docs)={sims}, {dt:.1f}s incl. load")
    except Exception as ex:                                   # noqa: BLE001
        ok = False
        print(f"[FAIL] embedder {EMB}: {type(ex).__name__}: {ex}")

    t0 = time.perf_counter()
    try:
        from sentence_transformers import CrossEncoder
        ce = CrossEncoder(RERANK)
        s = [round(float(x), 3) for x in ce.predict([(q, d) for d in docs])]
        dt = time.perf_counter() - t0
        log("_test", "check_rerank", seconds=dt, n_items=2, note=RERANK)
        print(f"[ok] reranker  {RERANK}: scores={s}, {dt:.1f}s incl. load")
    except Exception as ex:                                   # noqa: BLE001
        print(f"[skip] reranker {RERANK}: {type(ex).__name__}: {ex}\n"
              "       -> arm 1 will run without the cross-encoder stage")

    n = sum(1 for _ in LOG.open()) if LOG.exists() else 0
    print(f"[{'ok' if n else 'FAIL'}] cost log  {LOG}: {n} row(s)")
    print("\nSTEP 0 PASSED" if ok and n else "\nSTEP 0 NOT PASSED (see above)")


if __name__ == "__main__":
    main()
