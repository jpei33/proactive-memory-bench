"""Done-when checks for 3.1 and 3.2.

    python -m memory.check --ws ando
3.1  oracle (each plant's evidence as one chunk) -> full delivery for every fact plant;
     window-only -> no delivery for every cross plant.
3.2  ando/t2/011's C chunk contains oli's AND-341 question and "I'll take it", with Cstar and
     (if data/cache/parents_<ws>.json exists) inferred parents. Also prints chunk counts.
"""
from __future__ import annotations

import argparse

from memory.base import (deliveries, fact_plants, load_msgs, load_plants, make_chunk, visible,
                         window)
from memory.chunkers import chunk_A, chunk_B, chunk_C, gold_parents
from memory.linker import load_parents


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", default="ando")
    a = ap.parse_args()
    msgs, plants = load_msgs(a.ws), load_plants(a.ws)
    by_id = {m["msg_id"]: m for m in msgs}
    ok = True

    print("== 3.1 oracle / window-only delivery")
    for p in fact_plants(plants):
        trig = by_id[p["trigger_msg"]]
        q = trig["seq"]
        win = [m["msg_id"] for m in window(msgs, q, trig["channel"])]
        oracle = [make_chunk(f"O:{g['group']}", [by_id[i] for i in g["msgs"]]) for g in p["evidence_groups"]]
        d_or = deliveries(visible(oracle, q, by_id), win, p)
        d_win = deliveries([], win, p)
        flag = ""
        if d_or["all"] != "full":
            flag += "  <-- oracle not full"; ok = False
        if p.get("bucket") == "cross" and d_win["all"] != "none":
            flag += "  <-- cross plant visible in window"; ok = False
        print(f"  {p['plant_id']:<12} {p['type']:<16} {str(p.get('bucket')):<6} "
              f"oracle={d_or['all']:<7} window={d_win['all']:<7} (origin: {d_win['origin']}){flag}")

    print("\n== 3.2 chunk counts")
    A, B, Cs = chunk_A(msgs), chunk_B(msgs), chunk_C(msgs, gold_parents(msgs))
    print(f"  A {len(A)}  B {len(B)}  Cstar {len(Cs)}")
    inferred = load_parents(a.ws)
    variants = [("Cstar", Cs)] + ([("C", chunk_C(msgs, inferred))] if inferred else [])
    if not inferred:
        print(f"  (no data/cache/parents_{a.ws}.json yet; run python -m memory.linker --ws {a.ws})")
    target = f"{a.ws}/t2/011"
    if a.ws == "ando":
        for name, chunks in variants:
            c = next(c for c in chunks if c.chunk_id == f"C:{target}")
            good = "AND-341" in c.text and "I'll take it" in c.text
            ok &= good
            print(f"\n  {name} chunk for {target}: {'OK' if good else 'MISSING PARENT'}\n    " +
                  c.text.replace("\n", "\n    "))
    print("\n== 3.3 D (topic segments) and E (rewrite)")
    from memory.rewrite import chunk_E, load_rewrite
    from memory.segment import chunk_D, load_segments
    seg, rw = load_segments(a.ws), load_rewrite(a.ws)
    if seg is None:
        print(f"  (no segments yet; run python -m memory.segment --ws {a.ws})")
    else:
        D = chunk_D(msgs, seg)
        print(f"  D {len(D)} chunks, avg {sum(len(c.source_msgs) for c in D) / len(D):.1f} msgs")
        if a.ws == "ando":
            c = next(c for c in D if f"{a.ws}/t2/011" in c.source_msgs)
            both = f"{a.ws}/t2/010" in c.source_msgs
            print(f"  D chunk holding t2/011 also holds t2/010 (the question): {both}")
    if rw is None:
        print(f"  (no rewrite yet; run python -m memory.rewrite --ws {a.ws})")
    else:
        E = chunk_E(msgs, rw)
        print(f"  E {len(E)} statements from {len(rw)} messages")
        if a.ws == "ando":
            for mid, want, need_src in ((f"{a.ws}/t2/011", ("AJ", "AND-341"), f"{a.ws}/t2/010"),
                                        (f"{a.ws}/t4/006", ("free",), f"{a.ws}/t3/035")):
                st = [c for c in E if c.chunk_id.startswith(f"E:{mid}:")]
                txt = " | ".join(c.text for c in st)
                good = any(all(w.lower() in c.text.lower() for w in want) and need_src in c.source_msgs for c in st)
                ok &= good
                print(f"  {'OK  ' if good else 'FAIL'} {mid}: {txt or '(skipped)'}\n       sources: {[c.source_msgs for c in st]}")

    print("\nALL CHECKS PASS" if ok else "\nSOME CHECKS FAILED")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
