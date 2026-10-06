# Findings (draft, Day 5)

Setup in one line: 4 simulated Slack workspaces (876 messages), 303 decision points (36 INTERVENE
plants, 13 TRACK plants, 33 decoys, 150 ordinary, 71 follow-ups), a fixed Sonnet judge, and 22 memory
conditions: no memory (S0), 5 chunkers x 3 retrievers, gold reply links (Cs2), two grep-style agents,
two extra budgets, and an oracle facts box (OR). Gold labels: 132 human-adjudicated + 171 from a
cross-family LLM labeler (see human_agreement.md).

## 1. What the agent sees is decided by chunking, not by search
Proactive retrieval (the agent searches from the last 3 messages, unprompted), % of queries where all
evidence for the fact reached the agent at 1,500 tokens (36 plants + 155 probe triggers):
spread across chunkers **41 pts [36, 47]**, across retrievers **7 pts [3, 11]**; difference 35 pts [28, 41].
Per-message chunks deliver explicit statements 84% of the time but ellipsis answers 18% and emoji
reactions 13%; 6-message windows: 67 / 67; write-time rewrite: 73 / 73.
When asked directly (the probe question as query) every chunker delivers 82-100%: the gap exists only
when the agent has to notice on its own.
Embeddings are not better than BM25 on context-free replies: on ando-p16, "nah hand it to me" ranks
193/245 under BM25 and 237/245 under embeddings.

## 2. The "I did" problem, caught in the act
xai-p10 (repeat_question, cross-channel). Sep 30, #infra:
> wen: Who's owning fabric incident on-call for kestrel right now? I need a name on the rota...
> lucia: I'll take it.

Oct 12, #kestrel-run (the trigger):
> mateo: ...I'm seeing IB link flaps on a couple of the dataloader nodes. Who's on call for fabric incidents today?

- A3 (per-message + hybrid) retrieved Wen's question but not the answer, and concluded the opposite:
  *"the memory has no current answer (Wen asked the same on Sep 30 with no recorded reply)"* -> IGNORE.
- E1 (rewrite + BM25) retrieved the rewrite of the question, *"Wen needs to identify the on-call fabric
  incident owner"*, but not the rewrite of the answer (*"lucia is taking on-call ownership..."*) -> IGNORE.
- AG-grep searched `on call|on-call|oncall|fabric`, then `read_around(xai/t2/007)`, saw "I'll take it"
  under the question, and answered: *"on Sep 30 in #infra Lucia said 'I'll take it' when Wen asked who
  owned fabric on-call, so Lucia is the answer"* -> INTERVENE.
At the trigger, A3 and E1 both stayed silent; the grep agents caught it immediately. (E1 recovered on a
follow-up message; A3 never did.) Over all conditions, 9 of 22 missed this plant entirely, including A1,
A3, C1, C3, D2, E3 and S0. Reading around a hit is what reconstructs the question-answer pair.

## 3. For fact conflicts, most memories reach ~90%; missed deadlines are invisible to retrieval
Catch rate (INTERVENE at the conflict or within 2 messages):

| plant type | n | no memory | best retrieval cells | C1 (guessed links) | oracle facts box |
|---|---|---|---|---|---|
| contradiction | 11 | 36% | 100% | 82% | 100% |
| repeat_question | 8 | 0% | 88% | 62% | 88% |
| stale_quote | 10 | 40% | 90% | 70% | 100% |
| deadline_passed | 7 | 0% | 0-43% (E1: 0%) | 0% | 100% |

On the 29 fact plants, E1 and B3 each catch 26 (90%). On the 7 deadline plants, every retrieval memory
fails because the evidence is an absence. E1 had Frida's commitment in memory (*"send design partners the
migration guide by Fri Sep 11"*) on Mon Sep 14 and said *"no passed check point"*. The oracle, which lists
open items with check points, said *"The Sep 11 check point for Frida's migration guide has passed with no
sign it was sent"*. Retrieval answers "what was said"; deadlines need "what should have happened".

Tested directly (5.3): adding the open items with their check points to E1's memory (E1+OI) lifts
deadline catches from 0% to 50% (3/6); the agent's own earlier TRACK notes (E1+T) reach 29% (2/7).
The same open-item list added to B3 does not help (43% -> 43%) and costs elsewhere (stale_quote 80% -> 60%,
false alarms 5.6 -> 12.9 per 100). The oracle shows the same items but in a short facts-only box and
catches 7/7. So explicit tracking is necessary but not sufficient: buried under 1,500 tokens of retrieved
chat, the judge still misses half the passed deadlines. How the tracker is presented matters.

## 4. Precision, not recall, is the bottleneck once memory works
Perfect memory (OR) catches 97% of conflicts but has the most false alarms (13.8 severity-weighted per
100 decisions; 15 of them on ordinary chatter) and flags the same conflict again on the next message for
69% of plants. Raising E1's budget to 4,000 tokens lifts delivery 83% -> 94% with no F1 gain and more
false alarms. The decoy that fools almost every condition is a correct quote of a just-changed value
(decoy_legit_change_quote). Across the 15 cells INTERVENE F1 spans .63-.75 with overlapping CIs; the
best observed are A3 .75, B3 .73, E1 .73.

## 4b. With enough decision points, delivery differences do carry into decisions
The 36 natural plants are too few to separate memory setups, and a rerun shows why: the same judge on
the same memory changes 14-16% of its labels, moving catch rates by up to 8 pts (B3 81% -> 72%) and
INTERVENE F1 by up to .08 (E1). So plant-level differences under ~10 pts are judge noise.

Paired probes fix the sample size: 142 minimal pairs over 21 facts, each a casual message stating a fact
with a wrong value (should INTERVENE) and the identical message with the current value (should IGNORE).

| condition | catch wrong value | false alarm on correct value | balanced acc. |
|---|---|---|---|
| no memory (S0) | 6% [2, 11] | 6% | 50 |
| A3 per message + hybrid | 72% [59, 84] | 27% | 73 |
| B3 windows + hybrid | 69% [62, 76] | 15% | 77 |
| Cs2 gold reply links | 69% [56, 80] | 18% | 76 |
| D2 topics + embeddings | 72% [59, 82] | 19% | 76 |
| E1 rewrite + BM25 | **82% [74, 90]** | 20% | 81 |
| AG-grep agent | 74% [62, 85] | **8%** | **83** |
| oracle facts box | 96% [92, 100] | 30% | 83 |

- E1 catches significantly more wrong values than B3 (+13 pts [+5, +22]) and Cs2 (+13 [+1, +27]); vs A3,
  D2 and the grep agent the difference is 8-11 pts with CIs touching 0.
- The difference is delivery: E1 delivered the evidence on 91% of pairs vs 56-70% for the others, and once
  delivered every condition catches 88-93%. No sign that E's rewrites hurt the judge.
- The grep agent has the best precision (8% false alarms): it searches only when something looks
  checkable, so it rarely second-guesses correct statements. It ties the oracle on balanced accuracy.
- More memory means more false alarms: the oracle flags 30% of correct statements, per-message chunks 27%.

## 5. Reply links only help when they are right; agents only help when they look
- Gold reply links (Cstar) deliver 64% vs 43% for Haiku-inferred links (C). The linker finds 90% of true
  parents but leaves only 26% of new-topic messages unlinked, so C chunks carry wrong context and fill the
  budget. At decision level C1 is the worst cell (58% caught; 13 of 15 misses "not surfaced").
- Grep agents catch 69% at about twice the cost per decision. They searched on 53% of plant triggers
  and 33% of ordinary messages; 8 of 11 misses are points where they did not search.
- Topic segmentation (D) puts "I'll take it" in a side conversation's segment when the reply comes
  after an interleaved message.

## Caveats
- 36 INTERVENE plants: catch-rate CIs are about +/-15 pts and a judge rerun moves them up to 8 pts;
  plant-level differences among memory setups are not significant. The paired probes (142 pairs) are the
  decision-level evidence; they are Haiku-written single messages, more explicit than natural plants.
- Simulated data only (real Slack/IRC check dropped for time).
- Follow-up points (2 per plant) are excluded from false-alarm metrics: the judge is stateless and
  repeats itself (see repeat_after in main.csv).
- Delivery is measured by message ids; for 20-30% of "full" deliveries the value itself is not stated in
  the memory text (implicit: "mine", "I'll take it").
- Robustness (results/robustness.csv):
  - Embedding model swap (OpenAI text-embedding-3-large -> local MiniLM): retrieval ranking holds
    (Spearman 0.92 over 15 cells; E still best, C still worst; retriever spread 7 vs 8 pts).
  - Judge swap (Sonnet -> Haiku) on 8 conditions: Haiku is a much weaker judge (catch rates drop 5-22 pts,
    false alarms 2-3x; OR false alarms 36 per 100). Rank correlation 0.67 (catch) / 0.81 (F1), but that is
    carried by the S0 and OR anchors: among the 6 memory conditions the order changes (Sonnet: B3 > D2 > E3;
    Haiku: E3 > C3 > D2 > B3). Retrieval-level conclusions are robust; which memory cell "wins" at the
    decision level is not, consistent with the overlapping CIs.

## Transcripts for the post
1. xai-p10 (finding 2): the "I'll take it" case, three conditions side by side.
2. ando-p06 (finding 3): commitment in memory, deadline not noticed; oracle notices.
3. ando-p16: "nah hand it to me" ranked 193/245 (BM25) and 237/245 (embeddings); grep("AND-341") finds it in one call.
