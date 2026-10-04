# How the benchmark makes facts hard to find

The benchmark asks whether an agent in a team chat can recall a fact that was settled
earlier, and act on it unprompted. For that question to say anything about memory, the
facts have to be stated the way people actually state them in chat, which is often
not in a form a search index can find.

## The problem this targets

In a codebase, things are referred to by exact, repeated names. `PaymentService` appears
verbatim wherever it is used, so grep finds it and an embedding model can place it.

In chat, the decisive message often contains neither the thing nor the value:

```
oli:  AND-341 needs an owner before launch, who can take it?
aj:   i'll grab it
```

A week later someone asks "who has AND-341 now?". The fact (AJ owns AND-341) lives in
"i'll grab it", which shares no words with the query, so BM25/grep miss it, and its
meaning on its own is "someone volunteered for something", so embedding search misses
it too. It is only recoverable if the answer is stored or retrieved together with the
question it answers.

The simulator plants facts in exactly these shapes, on purpose and with labels, so we
can measure which memory designs recover them.

## Evidence forms

Every fact statement in a ledger (`establish` or `update` event) has a `form`. The form
decides how many messages the statement takes and which words are banned from the key
message.

| Form | Messages | Banned in the key message | Example |
|---|---|---|---|
| `explicit` | 1 | nothing (control) | sara: "public launch is Sep 17" |
| `ellipsis` | question → short answer | the entity and the value | oli: "who can take AND-341?" → aj: "i'll grab it" |
| `reaction` | question → emoji | (no text at all) | olavo: "post says $20M Series A, 👍 if right?" → sara 👍 |
| `correction` | old value in passing → fix | the entity | olavo: "so for the 17th…" → sara: "let's make it the 24th" |
| `cross_ref` | proposal in one thread → adoption in a later thread | the value | alex (t3): "what if agents were free, $12 per human seat?" → sara (t4): "going with alex's pricing idea from monday" |
| `distributed` | part 1 → part 2 a few turns later | the entity (in part 2) | sara: "pricing is $12 per seat" … sara: "and agent actions get metered on top" |

Why each one is hard:

- **ellipsis**: the answer is meaningless without its question. For owner facts the value
  is the *speaker*, which never appears in the text.
- **reaction**: there is no text to index. Only the link to the target message carries meaning.
- **correction**: the new value appears without its entity; the entity appears next to
  the *old* value. Naive retrieval surfaces the stale value.
- **cross_ref**: the value and the decision live in different threads, days apart.
- **distributed**: no single message holds the whole fact; retrieving one part gives an
  incomplete or misleading answer.
- **explicit** is the control: every retriever should do fine on it.

## How "hard" is enforced, not just hoped for

1. **Ledger fields.** Each fact lists `keys`, the words that name its entity (e.g.
   `[and-341, "341", double-post]`). History entries can add `match`, a regex for
   spotting the value in text (e.g. `'1,?140'`, `'\b15\b'`). Without `match`, a pattern is
   built from the value, including date forms like "24th" and "the 24".
2. **Form expansion** (`expand_forms`). When a ledger loads, each non-explicit statement
   gets its helper message (the question, the setup, the proposal, part 2) scheduled as
   an extra turn, in the right thread. The whole statement is tagged as one *evidence
   group*, e.g. `and341_owner@t2/011` = [t2/010, t2/011].
3. **Per-form instructions** (`build_schedule`). The writer model gets a form-specific
   instruction ("answer in at most 6 words, don't name the thing") plus `forbid` and
   `require` patterns built from `keys`/`match`. A message that uses a banned word, or
   misses a required value, is resampled.
4. **Filler can't leak values.** Every unscripted message is checked against every
   tracked value, so a fact can't accidentally be restated in plain words between its
   evidence and the moment it matters.
5. **Verification** (`world/verify.py`) re-checks every group after generation: the
   answer really omits the entity, the correction really contains the new value, the
   proposal really sits in another thread, and nothing restates the value before a plant.

One special case: when someone reassigns a task to themselves ("nah hand it to me"),
the value is the speaker's own name, so the correction is not required to contain it.

## Channel structure

Whether a reply can be linked to its question depends on what the chat exposes, so each
thread has a `structure`:

- `threaded`: replies sit in Slack threads; the link is visible (`thread_ts`).
- `flat`: everything in the main channel; links must be inferred.
- `interleaved`: flat, plus an unrelated side conversation woven in. Events marked
  `gap: true` are forced to have a side message between question and answer, so
  "answer = the next message" heuristics fail.

Emoji reactions always keep their link, as in Slack.

## What gets measured

Each plant records **all** evidence groups that state the current value before its
trigger, and which of them is the *origin* (the statement that set the value).
Restatements by other messages (e.g. someone repeating the new date) count as extra
routes to the fact, and plants that have them are marked `restated: true`.

A memory system "delivers" a fact when every message of at least one evidence group is in
the context it hands the judge:

- **full**: the whole group (question + "i'll grab it"),
- **partial**: only part of it ("i'll grab it" alone, which is useless),
- **none**.

Delivery is computed automatically from message ids, so it costs nothing to score
every chunking × retriever combination. The judge model is only needed to see whether
delivered facts get acted on.

## Expected effect per memory design

| Memory design | Expected on hard forms |
|---|---|
| Per-message chunks | Fails on ellipsis and reactions with any retriever (the answer is indexed alone). |
| Sliding windows | Works when question and answer are adjacent; breaks on interleaved channels and cross_ref. |
| Reply-linked chunks (message + parent) | Recovers ellipsis/reaction/correction if links are known; the gap between gold and inferred links measures disentanglement. |
| Topic segments | Good on clean threads; interleaving splits or mixes topics. |
| Write-time rewrite ("AJ took ownership of AND-341") | Should recover most forms, at the cost of one LLM call per message. |
| Agent with grep + read-around | Can recover ellipsis by grepping "341" and reading the next messages, if it decides to search at all. |

## Current counts (from the ledgers)

- 49 plants (36 INTERVENE, 13 TRACK) and 33 decoys across 4 workspaces.
- 29 fact plants by origin form: explicit 4, ellipsis 5, reaction 3, correction 8,
  cross_ref 5, distributed 4. Another 7 `deadline_passed` plants depend on commitments.
- Too few per form for strong claims from plants alone, so retrieval-only "probe
  triggers" (messages that mention an entity without its value, used only as queries)
  raise the per-form n to about 15.

## Status

- Done: ledger forms, keys/match, thread structure, form expansion, per-form
  instructions (steps 1.1–1.6).
- Next: reply links and reaction rows during generation, plus enforcing `forbid`/`require`
  (1.7); Slack threads, interleaving, global ordering, and evidence groups in
  `plants.jsonl` (1.8); generation and `verify.py` (1.9–1.10).
