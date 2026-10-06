"""Cached, retrying wrapper around the Anthropic Messages API.

Every LLM call in the project goes through `complete()`:
the simulator, memory writers, probe reader and judge.

- Disk cache: the full request (+ seed) is hashed; the response is stored under
  data/cache/llm/. Re-running a script re-uses identical calls for free.
  Change `seed` to force a fresh sample for the same prompt (e.g. on regeneration).
- Retries: rate limits, overload and connection errors back off and retry.
- Usage: every result carries token counts; USAGE keeps running totals per model.

Quick test:  python -m sim.llm
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from tenacity import (retry, retry_if_exception, stop_after_attempt,
                      wait_random_exponential)

load_dotenv()

CACHE_DIR = Path(os.environ.get("LLM_CACHE_DIR", "data/cache/llm"))
USAGE: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
_USAGE_LOCK = threading.Lock()  # complete() may be called from several threads
_client: anthropic.Anthropic | None = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    return _client


@dataclass
class Result:
    text: str                      # concatenated text blocks
    in_tok: int
    out_tok: int
    cache_read_tok: int = 0        # prompt-cache hits (Anthropic-side)
    cache_write_tok: int = 0
    stop_reason: str = ""
    content: list = field(default_factory=list)  # raw blocks as dicts (for tool use)
    latency_s: float = 0.0
    cached: bool = False           # served from our disk cache
    model: str = ""

    @property
    def usage(self) -> dict:
        return {"in_tok": self.in_tok, "out_tok": self.out_tok,
                "cache_read_tok": self.cache_read_tok, "cache_write_tok": self.cache_write_tok}


def _retryable(e: BaseException) -> bool:
    if isinstance(e, (anthropic.RateLimitError, anthropic.APIConnectionError,
                      anthropic.APITimeoutError, anthropic.InternalServerError)):
        return True
    return isinstance(e, anthropic.APIStatusError) and e.status_code in (429, 500, 502, 503, 529)


@retry(retry=retry_if_exception(_retryable), wait=wait_random_exponential(min=2, max=60),
       stop=stop_after_attempt(8), reraise=True)
def _call(req: dict):
    return client().messages.create(**req)


def complete(system: str | None, messages: list[dict] | str, *, model: str | None = None,
             max_tokens: int = 1024, seed: int = 0, effort: str | None = None,
             tools: list[dict] | None = None, tool_choice: dict | None = None,
             cache_system: bool = False,
             use_cache: bool = True) -> Result:
    """One Messages API call, served from disk cache when the identical request was made before.

    messages: a list of {"role", "content"} dicts, or a plain string for a single user turn.
    cache_system: mark the system prompt for Anthropic prompt caching (use for the judge rubric).
    seed: not sent to the API; only part of the cache key, so a new seed forces a new sample.
    There is no temperature setting (the current SDK/API has none); reruns are made
    reproducible by the disk cache instead.
    """
    model = model or os.environ["SIM_MODEL"]
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    req: dict = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        req["system"] = ([{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
                         if cache_system else system)
    if effort:  # "low" | "medium" | "high" | ... ; omitted = API default
        req["output_config"] = {"effort": effort}
    if tools:
        req["tools"] = tools
    if tool_choice:
        req["tool_choice"] = tool_choice

    key = hashlib.sha256(json.dumps({"req": req, "seed": seed}, sort_keys=True, default=str)
                         .encode()).hexdigest()
    path = CACHE_DIR / key[:2] / f"{key}.json"

    if use_cache and path.exists():
        try:
            res = Result(**json.loads(path.read_text()))
            res.cached = True
            return res
        except (json.JSONDecodeError, TypeError):    # torn write from a parallel run: redo the call
            pass

    t0 = time.time()
    r = _call(req)
    u = r.usage
    res = Result(
        text="".join(b.text for b in r.content if b.type == "text"),
        in_tok=u.input_tokens, out_tok=u.output_tokens,
        cache_read_tok=getattr(u, "cache_read_input_tokens", 0) or 0,
        cache_write_tok=getattr(u, "cache_creation_input_tokens", 0) or 0,
        stop_reason=r.stop_reason or "", content=[b.model_dump() for b in r.content],
        latency_s=round(time.time() - t0, 3), model=model,
    )
    with _USAGE_LOCK:
        tot = USAGE[model]
        for k, v in res.usage.items():
            tot[k] += v
        tot["calls"] += 1

    if use_cache:
        path.parent.mkdir(parents=True, exist_ok=True)
        d = res.__dict__.copy()
        d.pop("cached")
        tmp = path.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps(d))
        os.replace(tmp, path)                        # atomic: readers never see a half-written file
    return res


def parse_json(text: str):
    """Pull the first JSON object/array out of a model reply (tolerates ```json fences and prose)."""
    s = text.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1].rsplit("```", 1)[0]
    for open_c, close_c in (("{", "}"), ("[", "]")):
        i, j = s.find(open_c), s.rfind(close_c)
        if i != -1 and j > i:
            try:
                return json.loads(s[i:j + 1])
            except json.JSONDecodeError:
                continue
    dec = json.JSONDecoder()                     # fallback: first object that decodes, ignoring trailing text
    for i, ch in enumerate(s):
        if ch in "{[":
            try:
                return dec.raw_decode(s[i:])[0]
            except json.JSONDecodeError:
                continue
    raise ValueError(f"no JSON found in: {text[:200]!r}")


if __name__ == "__main__":
    r1 = complete(None, "Say 'ready' and nothing else.", max_tokens=20)
    r2 = complete(None, "Say 'ready' and nothing else.", max_tokens=20)
    print(f"model={r1.model} text={r1.text!r} in={r1.in_tok} out={r1.out_tok} "
          f"latency={r1.latency_s}s cached={r1.cached}")
    print(f"second call cached={r2.cached} (should be True)")
    print("usage totals:", {m: dict(v) for m, v in USAGE.items()})
