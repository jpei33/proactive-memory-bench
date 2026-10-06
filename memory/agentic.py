"""Agentic arms: the judge searches the history itself with tools instead of getting retrieved memory.

    python -m memory.agentic --point ando/t6/032 --arm AG-grep     # 4.2 check: print the tool chain

Arms
  AG-grep  grep_history + read_around               (the Cursor-style "grep" agent)
  AG-both  grep_history + read_around + semantic_search
Tools only see messages with seq < the decision point's seq (the window is already in the prompt).
At most MAX_CALLS tool calls; then the judge must answer without tools.
"Delivered" = window ids ∪ every msg_id any tool returned.
"""
from __future__ import annotations

import json
import re

from memory.base import line

GREP = {"name": "grep_history",
        "description": "Case-insensitive regex search over earlier messages in this workspace (all channels). "
                       "Returns up to 10 matches, most recent first, as [msg_id] day #channel speaker: text.",
        "input_schema": {"type": "object", "properties": {"pattern": {"type": "string"}}, "required": ["pattern"]}}
READ = {"name": "read_around",
        "description": "Show the messages just before and after msg_id in its channel, plus replies and "
                       "reactions to it.",
        "input_schema": {"type": "object", "properties": {"msg_id": {"type": "string"}, "n": {"type": "integer"}},
                         "required": ["msg_id"]}}
SEM = {"name": "semantic_search",
       "description": "Search earlier messages by meaning. Returns up to 5 messages.",
       "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}
ARMS = {"AG-grep": [GREP, READ], "AG-both": [GREP, READ, SEM]}
MAX_CALLS = 4

TOOL_NOTE = """

You have tools to search earlier messages in this workspace. Use them when the latest message touches a
fact, owner, date, number or commitment you may need to check against history (at most {MAX} calls).
When you are done, reply with the JSON answer as plain text. It is not a tool: never call a tool
named json or answer."""


def fmt(m):
    return f"[{m['msg_id']}] {line(m)}"


class History:
    """The searchable past at one decision point."""

    def __init__(self, msgs, q_seq, ws=None):
        self.past = [m for m in msgs if m["seq"] < q_seq]
        self.by_id = {m["msg_id"]: m for m in self.past}
        self.ws, self.q_seq = ws, q_seq
        self.returned: list[str] = []

    def grep_history(self, pattern: str) -> str:
        try:
            rx = re.compile(pattern, re.I)
        except re.error:
            rx = re.compile(re.escape(pattern), re.I)
        hits = [m for m in reversed(self.past) if rx.search(m["text"])][:10]
        self.returned += [m["msg_id"] for m in hits]
        return "\n".join(fmt(m) for m in hits) or "(no matches)"

    def read_around(self, msg_id: str, n: int = 3) -> str:
        m = self.by_id.get(msg_id)
        if not m:
            return f"(no earlier message {msg_id})"
        n = max(1, min(int(n or 3), 8))
        ch = [x for x in self.past if x["channel"] == m["channel"]]
        i = ch.index(m)
        around = ch[max(0, i - n): i + n + 1]
        replies = [x for x in self.past if x.get("reply_to") == msg_id and x not in around]
        out = around + replies
        self.returned += [x["msg_id"] for x in out]
        return "\n".join(("> " if x is m else "") + fmt(x) for x in out)

    def semantic_search(self, query: str) -> str:
        from memory.base import make_chunk
        from memory.retrievers import rank_emb
        chunks = [make_chunk(f"A:{m['msg_id']}", [m]) for m in self.past]
        top = [chunks[i] for i in rank_emb(chunks, query)[:5]] if chunks else []
        ids = [c.source_msgs[0] for c in top]
        self.returned += ids
        return "\n".join(fmt(self.by_id[i]) for i in ids) or "(nothing)"

    def call(self, name, args):
        try:
            if name == "grep_history":
                return self.grep_history(str(args.get("pattern", "")))
            if name == "read_around":
                return self.read_around(str(args.get("msg_id", "")), args.get("n", 3))
            if name == "semantic_search":
                return self.semantic_search(str(args.get("query", "")))
        except Exception as e:                        # a bad tool call is the agent's problem, not a crash
            return f"(tool error: {e})"
        return f"(unknown tool {name})"


def _clean(blocks):
    """Assistant content blocks to send back: drop None fields the API doesn't want."""
    return [{k: v for k, v in b.items() if v is not None} for b in blocks]


def run_agent(system: str, user: str, hist: History, arm: str, model: str, effort: str = "low", seed: int = 0):
    """-> (final Result, trace list of {tool, input}, total in/out/cache tokens)"""
    from sim.llm import complete
    tools = ARMS[arm.split("~")[0]]
    messages = [{"role": "user", "content": user}]
    trace, tot = [], {"in": 0, "out": 0, "cache_read": 0, "latency": 0.0}
    sysmsg = system + TOOL_NOTE.replace("{MAX}", str(MAX_CALLS))
    for step in range(MAX_CALLS + 1):
        last = len(trace) >= MAX_CALLS
        r = complete(sysmsg, messages, model=model, max_tokens=2000, effort=effort, tools=tools,
                     tool_choice={"type": "none"} if last else None, cache_system=True, seed=seed)
        tot["in"] += r.in_tok; tot["out"] += r.out_tok; tot["cache_read"] += r.cache_read_tok
        tot["latency"] += r.latency_s
        uses = [b for b in r.content if b.get("type") == "tool_use"]
        if (not uses or last) and not r.text.strip():
            # finished searching but wrote no answer: ask once more, plainly
            messages.append({"role": "assistant", "content": _clean(r.content) or [{"type": "text", "text": "(no answer)"}]})
            if uses:
                messages.append({"role": "user", "content": [
                    {"type": "tool_result", "tool_use_id": b["id"], "content": "(tool budget used up)"} for b in uses]
                    + [{"type": "text", "text": "Answer now with only the JSON."}]})
            else:
                messages.append({"role": "user", "content": "Answer now with only the JSON."})
            r2 = complete(sysmsg, messages, model=model, max_tokens=2000, effort=effort, tools=tools,
                          tool_choice={"type": "none"}, cache_system=True, seed=seed)
            tot["in"] += r2.in_tok; tot["out"] += r2.out_tok; tot["cache_read"] += r2.cache_read_tok
            tot["latency"] += r2.latency_s
            return r2, trace, tot
        if not uses or last:
            return r, trace, tot
        messages.append({"role": "assistant", "content": _clean(r.content)})
        results = []
        for b in uses:
            if b["name"] not in {t["name"] for t in tools}:      # e.g. a made-up "json" tool
                tot["bad_tool"] = tot.get("bad_tool", 0) + 1
                out = "(there is no such tool; reply with your JSON answer as plain text)"
            elif len(trace) < MAX_CALLS:
                out = hist.call(b["name"], b.get("input") or {})
                trace.append({"tool": b["name"], "input": b.get("input")})
            else:
                out = "(tool budget used up; answer now)"
            results.append({"type": "tool_result", "tool_use_id": b["id"], "content": out})
        messages.append({"role": "user", "content": results})
    return r, trace, tot


def main():
    import argparse
    import os
    from dotenv import load_dotenv
    load_dotenv(".env")
    from judge.conditions import ws_data
    from judge.run import judge_one
    ap = argparse.ArgumentParser()
    ap.add_argument("--point", default="ando/t6/032")
    ap.add_argument("--arm", default="AG-grep")
    a = ap.parse_args()
    pts = {p["point_id"]: p for p in json.load(open("data/eval_points.json"))}
    p = pts[a.point]
    row = judge_one(p, a.arm, 1500, os.environ["JUDGE_MODEL"], "low")
    _, _, by_id, _ = ws_data(p["ws"])
    print(f"{a.point} [{a.arm}] decision message: {by_id[a.point]['speaker']}: {by_id[a.point]['text']}")
    for t in row["trace"]:
        print(f"  -> {t['tool']}({json.dumps(t['input'])})")
    print(f"  delivery={row['delivery']}  label={row['label']}  cited={row['cited_value']!r}\n  reason: {row['reason']}")
    print(f"  msgs returned by tools: {len(row['retrieved'])}; tokens in {row['in_tok']} out {row['out_tok']}")


if __name__ == "__main__":
    main()
