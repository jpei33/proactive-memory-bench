"""Reference-recovery queries for the private 'real' workspace (Step 2 of the 3-way plan).

    python -m eval.ref_extract          # -> data/real/ref_queries.jsonl (git-ignored) + counts

The real export has no reply links, quotes or message permalinks, so a "reference" is one of:

  artifact     a later message mentions the same PR / issue / commit / Linear ticket / URL as an
               earlier message. Target = every earlier message with that identifier outside the
               query's 15-message window. Clean ground truth; the main real-data query set.
  thread_root  a message in a Slack thread whose root has left the 15-message window. Target =
               the root (the reply parent in Slack's model). At most 3 queries per thread, evenly
               spaced, so long threads do not dominate.
  deictic      "earlier", "you said", "remember", ... Target = the earlier non-window message with
               the highest content-word overlap. NOISY and biased toward lexical retrievers (the
               target is picked lexically): report separately, never in the headline.

Hiding the pointer: identifiers (URLs, AND-123, #123) are replaced with "[ref]" in every part of
the query text. Query text follows judge.conditions.point_view: the last 2 window messages + the
referencing message (proactive query). Memory may only use messages before the query (seq < q).

Each row: {qid, kind, ws, seq, channel, query_msg_id, query, target_msg_ids, keys, distance,
conversation, bare}. distance = channel messages between the newest target and the query.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from memory.base import load_msgs, window

WS = "real"
OUT = Path("data/real/ref_queries.jsonl")
URL = re.compile(r"https?://[^\s)>\]\"'`]+")
TICKET = re.compile(r"\b(AND-\d+)\b", re.I)
HASHNUM = re.compile(r"(?<![\w/&])#(\d{2,6})\b")
SKIP_HOSTS = ("klipy.com", "giphy.com", "tenor.com")          # reaction gifs, not references
DEICTIC = re.compile(r"(?i)\b(earlier|above|as (?:i|we) (?:said|mentioned|discussed)|you said|"
                     r"we said|remember|last week|yesterday|like i said|following up)\b")
STOP = set("the a an and or but to of in on for with is are was were be been it this that i you we "
           "they he she my your our me us at as by from so not no do does did have has had can could "
           "would should will just like what when how why which who there here then than also about "
           "into out up if its it's i'm don't yeah ok okay".split())


def keys_of(text: str) -> set[str]:
    """Canonical identifiers in a message."""
    ks = set()
    for u in URL.findall(text):
        u = u.rstrip(".,;:!?")
        host = re.sub(r"^https?://", "", u).split("/")[0].lower()
        if any(h in host for h in SKIP_HOSTS):
            continue
        path = re.sub(r"^https?://[^/]+", "", u).split("?")[0].split("#")[0].rstrip("/")
        m = re.match(r"/([^/]+/[^/]+)/(pull|issues)/(\d+)", path)
        if "github.com" in host and m:
            ks.add(f"gh:{m.group(1).lower()}#{m.group(3)}")
            continue
        m = re.match(r"/([^/]+/[^/]+)/commit/([0-9a-f]{7})", path)
        if "github.com" in host and m:
            ks.add(f"ghc:{m.group(1).lower()}@{m.group(2)}")
            continue
        m = re.search(r"/issue/(AND-\d+)", path, re.I)
        if m:
            ks.add(f"lin:{m.group(1).upper()}")
            continue
        ks.add(f"url:{host}{path}")
    ks |= {f"lin:{t.upper()}" for t in TICKET.findall(text)}
    return ks


def hide(text: str) -> str:
    text = URL.sub("[ref]", text)
    text = TICKET.sub("[ref]", text)
    return HASHNUM.sub("[ref]", text)


def content(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z0-9'-]{2,}", text.lower()) if w not in STOP}


def query_text(msgs, q) -> tuple[str, list[str]]:
    w = window(msgs, q["seq"], q["channel"])
    prev = [m for m in w if m["msg_id"] != q["msg_id"]][-2:]
    return " \n".join(hide(m["text"]) for m in prev + [q]), [m["msg_id"] for m in w]


def main():
    msgs = load_msgs(WS)
    by_ch_pos = {}
    for ch in {m["channel"] for m in msgs}:
        for i, m in enumerate(x for x in msgs if x["channel"] == ch):
            by_ch_pos[m["msg_id"]] = i
    keys = {m["msg_id"]: keys_of(m["text"]) for m in msgs}
    rows = []

    def add(kind, q, targets, ks=()):
        qt, win = query_text(msgs, q)
        targets = [t for t in targets if t not in set(win)]
        if not targets:
            return
        newest = max(targets, key=lambda t: by_ch_pos.get(t, -1))
        same_ch = [t for t in targets if by_ch[t]["channel"] == q["channel"]]
        dist = (by_ch_pos[q["msg_id"]] - by_ch_pos[newest]) if same_ch else None
        rows.append({"qid": f"{kind}/{q['msg_id']}", "kind": kind, "ws": WS, "seq": q["seq"],
                     "channel": q["channel"], "query_msg_id": q["msg_id"], "query": qt,
                     "target_msg_ids": sorted(targets, key=lambda t: by_ch[t]["seq"]),
                     "keys": sorted(ks), "distance": dist, "conversation": q["channel"][1:],
                     "bare": len(content(hide(q["text"]))) < 2})

    by_ch = {m["msg_id"]: m for m in msgs}
    # artifact references
    for q in msgs:
        ks = keys[q["msg_id"]]
        if not ks:
            continue
        tg = [m["msg_id"] for m in msgs if m["seq"] < q["seq"] and keys[m["msg_id"]] & ks]
        add("artifact", q, tg, ks)
    # thread roots
    threads = defaultdict(list)
    for m in msgs:
        threads[m["thread_ts"]].append(m)
    for root, ms in threads.items():
        ms = sorted(ms, key=lambda m: m["seq"])
        cand = [q for q in ms[1:] if root not in {w["msg_id"] for w in window(msgs, q["seq"], q["channel"])}]
        if cand:
            pick = sorted({round(i * (len(cand) - 1) / 2) for i in range(3)}) if len(cand) >= 3 else range(len(cand))
            for i in pick:
                add("thread_root", cand[i], [root])
    # deictic (noisy)
    for q in msgs:
        if not DEICTIC.search(q["text"]):
            continue
        qc = content(hide(q["text"]))
        win = {w["msg_id"] for w in window(msgs, q["seq"], q["channel"])}
        best, score = None, 0.0
        for m in msgs:
            if m["seq"] >= q["seq"] or m["msg_id"] in win:
                continue
            mc = content(m["text"])
            j = len(qc & mc) / max(len(qc | mc), 1)
            if j > score:
                best, score = m["msg_id"], j
        if best and score >= 0.15:
            add("deictic", q, [best])

    OUT.write_text("".join(json.dumps(r) + "\n" for r in rows))
    k = Counter(r["kind"] for r in rows)
    print("queries per kind:", dict(k), " total", len(rows))
    for kind in k:
        rs = [r for r in rows if r["kind"] == kind]
        d = sorted(r["distance"] for r in rs if r["distance"] is not None)
        conv = Counter(r["conversation"] for r in rs)
        print(f"  {kind:<11} conversations={len(conv)} max/conv={max(conv.values())} "
              f"bare={sum(r['bare'] for r in rs)} cross-channel={sum(r['distance'] is None for r in rs)} "
              f"distance median={d[len(d)//2] if d else '-'} range={(d[0], d[-1]) if d else '-'} "
              f"targets/query={sum(len(r['target_msg_ids']) for r in rs)/len(rs):.1f}")
    print(f"-> {OUT}  (git-ignored)")


if __name__ == "__main__":
    main()
