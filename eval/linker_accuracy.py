"""Inferred (Haiku) vs gold reply parents, by thread structure.

    python -m eval.linker_accuracy --out results/linker.csv
Only messages a real system must guess (plain channel messages: not reactions, not thread replies).
  linked:   message really replies to something -> did we pick that parent?
  unlinked: message really starts something new -> did we say NONE?
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict

from memory.base import load_msgs
from memory.linker import load_parents
from sim.run_workspace import load

WSS = ["ando", "anthropic", "openai", "xai"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/linker.csv")
    a = ap.parse_args()
    agg = defaultdict(lambda: [0, 0, 0, 0])            # linked ok, linked n, unlinked ok, unlinked n
    for ws in WSS:
        msgs, par, d = load_msgs(ws), load_parents(ws), load(ws)
        struct = {t["id"]: t.get("structure", "flat") for t in d["threads"]}
        for m in msgs:
            if m["kind"] != "message" or m["thread_ts"]:
                continue
            for key in ((ws, struct[m["thread"]]), ("all", struct[m["thread"]]), ("all", "all")):
                s = agg[key]
                if m["reply_to"]:
                    s[0] += par.get(m["msg_id"]) == m["reply_to"]; s[1] += 1
                else:
                    s[2] += par.get(m["msg_id"]) is None; s[3] += 1
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ws", "structure", "linked_correct", "linked_n", "linked_acc",
                    "unlinked_correct", "unlinked_n", "unlinked_acc"])
        for (ws, st), (lo, ln, uo, un) in sorted(agg.items()):
            w.writerow([ws, st, lo, ln, round(lo / ln, 3) if ln else "", uo, un, round(uo / un, 3) if un else ""])
            if ws == "all":
                print(f"{st:<12} linked {lo}/{ln} ({lo / max(ln, 1):.0%})   unlinked {uo}/{un} ({uo / max(un, 1):.0%})")
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
