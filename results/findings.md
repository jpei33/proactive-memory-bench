# Findings

All workspaces, people and companies in the simulated data are fictional (see the disclaimer in the README).
Numbers come from `results/*.csv`; every judge decision is in `data/runs/`.

**Setup.** 4 simulated Slack-style workspaces (876 messages, 21 threads). 303 decision points: 49 planted
items (36 conflicts that need an INTERVENE, 13 commitments to TRACK), 33 decoys, 150 ordinary messages,
71 follow-up messages. A fixed Sonnet judge decides IGNORE / TRACK / INTERVENE at each point under 22 memory
conditions: no memory (S0); 5 chunkers x 3 retrievers; gold reply links (Cstar); two search-on-demand agents;
two extra token budgets; an oracle facts box (OR). Gold labels: 132 human-adjudicated + 171 from a
cross-family LLM labeler (`results/human_agreement.md`). Total API spend ~$80.

---

## 1. What the agent sees is decided by chunking, not by search  (solid)

Proactive retrieval (the agent queries with the last 3 messages, unprompted), % of queries where all
evidence for the fact reached the agent at 1,500 tokens; 36 plants + 155 probe triggers:

- spread across chunkers **41 pts [36, 48]** vs across retrievers **7 pts [2, 13]**; difference 35 pts
  [26, 44] with a bootstrap over the 28 underlying facts;
- holds with a different embedding model (OpenAI text-embedding-3-large vs local MiniLM: Spearman 0.92
  across the 15 cells; difference 34 pts [24, 42]);
- write-time rewrite (E) delivers the most (E1 87%); inferred reply links (C) the least (39-47%);
- token use is the same across chunkers (1,330-1,460 tokens), so E's lead is not a budget effect.

The "I did" problem shows up by evidence form (origin delivery, best retriever per chunker): per-message
chunks deliver explicit statements 84% of the time but ellipsis answers ("I'll take it") 18% and emoji
reactions 13%; 6-message windows 67 / 67; rewrite 73 / 73. Embeddings are not better than BM25 on
context-free replies: "nah hand it to me" ranks 193/245 under BM25 and 237/245 under embeddings.

When asked directly (the probe question as query) every chunker delivers 82-100%: the gap exists only when
the agent has to notice on its own.

## 2. Delivery predicts answers

A fixed reader answering the probe question from retrieved memory is correct 93% of the time when the
evidence was fully delivered and 3% when nothing was. Delivery is a valid proxy for what the agent can know.

## 3. On natural plants, memory setups cannot be ranked  (honest null)

Catch rate on the 36 planted conflicts (INTERVENE at the conflict or within the next 2 messages):
no memory 22%, the 15 strategies 58-81%, the oracle 97%. Intervals are about +/-15 pts, and rerunning the
same judge on the same memory changes 14-16% of labels and moves catch rates by up to 8 pts (B3 81% -> 72%).
So the differences between strategies on these plants are within noise.

By plant type, the 29 fact conflicts (contradiction, stale quote, repeat question) are caught 86-90% by
most memory setups (E1 26/29, B3 26/29, D2 25/29). The apparent lead of B and D overall comes from 3 of 7
missed-deadline plants (finding 5).

## 4. On targeted wrong-value probes, the delivery advantage carries into decisions  (targeted, post hoc)

142 paired probes over 21 facts: a message that states a fact with a wrong value (should INTERVENE) and the
identical message with the current value (should IGNORE). Results: `results/probe_table.md`.

- E1 catches 82% [74, 90] vs B3 69% and Cs2 69% (paired differences +13 pts, CIs exclude 0); vs A3, D2 and
  the grep agent the lead is 8-11 pts with CIs touching 0.
- The difference is delivery: E1 delivered the evidence on 91% of pairs vs 56-70% for the others, and once
  delivered every condition catches 88-93%.

Limits, stated plainly: this test was designed after seeing finding 3; it covers only "states a wrong value"
conflicts (no deadlines, no repeat questions), only far/cross positions, and Haiku-written single
messages with mostly invented wrong values. It shows that delivery matters for this conflict type; it does
not show that E makes better decisions overall.

## 5. Missed deadlines are invisible to retrieval

7 plants where a check point passed and nobody did the task. Retrieval memories catch 0-43% (E1 0/7);
the oracle, which lists open items with check points, catches 7/7. E1 had the commitment ("send the guide
by Fri Sep 11") in memory on Sep 14 and said "no passed check point". Adding the open-item list to E1's
memory lifts it to 3/6; the agent's own earlier TRACK notes to 2/7; the same list added to B3 does not help
(3/7) and adds false alarms. A tracker is necessary but not sufficient when it is buried in retrieved chat.

## 6. More memory makes the judge speak more, not more accurately

The oracle catches 97% of plants but has the most false alarms (13.8 per 100 decisions) and flags 30% of
correct statements on the paired probes; per-message chunks flag 27%. A 4,000-token budget raises E1's
delivery to 94% with no F1 gain. The search-on-demand agent has the fewest false alarms on the probes (8%):
it searches only when a message looks checkable (53% of plant triggers, 33% of ordinary messages).
The decoy that fools almost every condition is a correct quote of a just-changed value.

## 7. Reply links only help when they are right

Gold reply links (Cstar) deliver 61-67% vs 39-47% for links inferred by Haiku. The linker finds 90% of
true parents but leaves only 26% of new-topic messages unlinked, so its chunks carry wrong context. At the
decision level C1 is the weakest cell (58%; 13 of 15 misses "not surfaced"). Topic segmentation (D) puts
"I'll take it" into a side conversation's segment when the reply follows an interleaved message.

## 8. The judge model matters as much as the memory

Haiku as judge on the same memories catches 5-22 pts fewer plants and raises false alarms 2-3x (oracle:
36 per 100). Rank correlation with Sonnet is 0.67 (catch) / 0.81 (F1), carried by the no-memory and oracle
anchors; among memory setups the order changes (Sonnet B3 > D2 > E3, Haiku E3 > C3 > D2 > B3).

## 9. Reality check on real chat

50 real decision points from a team where people and AI agents work together (private data; aggregate
numbers only, `results/real_check.md`). Two labelers (Claude, GPT) each mark 5 cases as needing an
intervention but agree on only 2 (kappa 0.33). The same judge intervened on **0 of 50** under every model
and context length: no false alarms, but it missed both consensus cases. It saw the conflicting messages and
declined because they did not fit its rubric's idea of a conflict; both concern the agents' own work
(duplicate tickets from parallel agents, an agent contradicting its own diagnosis), a category the simulated
benchmark does not contain. Details and next steps: `notes/real_data_lessons.md`.

---

## Caveats

- Simulated data, 4 workspaces, written by one model family (Sonnet); the judge is the same family.
- 36 natural INTERVENE plants: too few to rank memory setups; judge noise is up to 8 pts.
- Paired probes are targeted and post hoc (finding 4).
- Follow-up messages are excluded from false-alarm metrics: the judge is stateless and repeats itself
  after catching a conflict (`repeat_after` in `results/main.csv`).
- Delivery is measured by message ids; for 20-30% of "full" deliveries the value is implicit ("mine").
- Gold labels: one human plus an LLM labeler; first-pass human recall on planted conflicts was 66%.
- Real-data check: 50 cases, 2 consensus positives, one team.

## Transcripts worth showing

1. **xai-p10, "I'll take it".** Wen: "Who's owning fabric incident on-call?" Lucia: "I'll take it." Twelve
   days later in another channel: "Who's on call for fabric incidents today?" Per-message memory retrieved
   only the question and concluded "no recorded reply"; the grep agent searched `on call`, read around the
   hit, found "I'll take it" and intervened. 9 of 22 conditions missed this plant entirely.
2. **ando-p06, missed deadline.** Commitment in memory, check point passed, judge says "no passed check
   point"; the oracle says "the Sep 11 check point has passed with no sign it was sent".
3. **ando-p16, "nah hand it to me".** Ranked 193/245 (BM25) and 237/245 (embeddings); a single
   `grep("AND-341")` finds it.
