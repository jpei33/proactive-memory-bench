# Real-data check: lessons and ideas for the next benchmark

Working notes for the final write-up (findings + future work). Status: for discussion, not final.
The source data is private (internal team chat shared by a contact, kept in git-ignored `data/real/`).
This file therefore contains no message text, names, ticket numbers or links: only aggregate numbers,
case ids and generic descriptions. Numbers: `results/real_check.md`; code: `eval/real_check.py`.

## 1. What we ran

- 50 decision points from 10 real conversations where people and several AI agents work together.
  Each case = one thread (median 17 earlier messages, max 76) + one new message.
- Reference labels: a Claude first pass (5/50 positive) and our cross-family GPT labeler (5/50).
  Agreement 88%, kappa 0.33; both agree on only 2 positives (cases 005, 023). No human pass
  (optional 5-minute check of those 2 cases is still open).
- Our fixed judge, same prompt and rubric as the benchmark, four conditions: Sonnet with the full thread,
  Sonnet with the last 15 messages, Haiku, GPT.

## 2. What we found

1. **The judge never intervened: 0/50 under every condition** (TRACK on 0-8 cases, the rest IGNORE).
   On simulated data the same judge intervened on ~10-17% of points with memory.
2. **This is not a missing-context problem for the clear cases.** In the full-thread condition the
   judge saw every message the labelers saw. For both consensus cases the evidence is inside the thread,
   and the judge's own reasons show it noticed it but declined because it was "not a contradiction of a
   team fact", had "no owner or check point", or "the humans are already noticing it". The rubric's
   categories (team fact, repeat question, tracked commitment, @-mention) don't fit these conflicts.
3. **Zero false alarms is not a win by itself.** A judge that never speaks gets 0 false alarms and is
   right ~90% of the time at this base rate. The small genuine positive: across 45 negatives (technical
   debugging, banter, long agent replies, frustrated messages) it never invented a conflict.
4. **Over-flagging vs silence are two faces of one issue.** In simulation, messages touching a tracked
   fact triggered interventions, sometimes too eagerly (oracle flagged 30% of correct statements in the
   paired probes). In real chat there are no "facts" in the rubric's sense, so it stays silent. Behaviour
   is driven by whether a message matches the rubric's notion of a conflict, not by calibrated noticing.
   Do not present over-flagging as a general property of the judge.
5. **Real conflicts are ambiguous.** Two model labelers agree on 2 of the 8 cases either one flags
   (kappa 0.33), versus kappa 0.85+ and 90% planted-conflict recall in simulation.
6. **Real conflicts are a different kind.** The candidate conflicts concern the agents' own claims and
   work, not people changing dates, owners or numbers.

## 3. What the benchmark does not cover (seen in the real data)

Who is in the chat
- AI agents as participants. Simulated workspaces are people-only with one silent judge.
- Several agents who could speak, and the question of which one should (case 010's expected note says
  it should come from a different agent than the one involved).

What counts as a conflict
- An agent contradicting its own earlier statement or diagnosis (023, 015).
- An agent promising an action the thread already showed it cannot take (034).
- Duplicate work from agents acting in parallel, e.g. several tickets for one request (005).
- A commitment dropped through a misread, e.g. an agent taking a joke literally (010).
- Conflicts in reasoning (diagnoses, hypotheses, root causes) rather than in a single checkable value.

Where the truth lives
- System state outside chat: whether a ticket exists, whether an integration is down, what a trace
  shows. Our ledger assumes every true fact was said in chat.
- Links between incidents across threads, rather than restated facts.

What a good intervention looks like
- Proposing an action ("want me to close the duplicates?"), not just correcting a value.
- Surfacing evidence when people disagree, which our rubric tells the agent to stay out of.

What the messages look like
- Long technical agent messages (markdown, links, code identifiers) next to very short or frustrated
  human messages; off-topic replies; threads spanning days.

Labels and base rate
- No ground truth by construction; ~10% positive; low labeler agreement; too few positives (50 cases)
  to measure catch rates.

## 4. Ideas for benchmark v2 (most valuable first)

1. **Agents as participants + agent-made plants.** 1-3 agent personas per workspace that answer, take
   tasks and file tickets, and sometimes err. New plant types: agent self-contradiction, impossible
   promise, parallel duplicate, dropped commitment. Matching decoys (agent self-correction, duplicate
   already handled) so false alarms stay measurable. Smallest useful version: 2 agent personas and the
   4 plant types in 1-2 workspaces (~1 day, reuses simulator + judge pipeline).
2. **Wider rubric, tested honestly.** Redefine INTERVENE to include agents' claims/actions conflicting
   with earlier messages or system state. Freeze it before evaluating on real data; do not tune it on the
   2 consensus cases.
3. **Chat + tool memory.** Add system state to the ledger (tickets, integration status, deploys, PRs)
   and let memory retrieve tool records as well as chat. Extends the chunking x retriever question.
4. **Score the intervention content.** Short LLM-graded checklist per plant: right evidence cited,
   right action proposed, right agent speaking. Keep the label metric primary.
5. **A proper real-data test set.** A few hundred cases from the same source (still private); a
   one-page definition of "should intervene" with examples; 2 labelers who know the team + the GPT
   labeler; report agreement. Inject paired conflict/control probes into real threads to measure
   sensitivity on real chat style without labeling.
6. **Messier simulated chat.** Long agent replies, short/frustrated humans, off-topic tangents,
   multi-day threads; re-check that the retrieval results hold.

Keep unchanged: chunking x retriever grid, delivery metrics, paired probes, judge noise floor,
cross-family labeling.

## 5. Open questions to discuss

- Is the 0/50 result the rubric (category mismatch) or the judge's threshold for speaking up? A
  rubric-only change on real data would tell, but with 2 positives it is an illustration, not a result.
- How much of the real data could be quoted or paraphrased publicly? Until cleared: numbers and generic
  descriptions only.
- Should v2 keep one silent AI teammate as the judge, or let one of the participating agents judge
  itself (self-monitoring) vs a separate monitor agent?
- For multi-agent chats: who should intervene, and is "another agent already noticed" an IGNORE?
- What is the right unit of evidence when truth lives in tools: retrieve tool records, or give the
  judge tool access (like the grep agent) to query them?
- Paired probes injected into real threads (~$1): run before the write-up, or leave as future work?

## 6. Draft text for the post ("Reality check" section)

"On 50 real decision points from a team where people and AI agents work together, the same judge never
intervened. It saw the full thread, including the conflicting messages, and declined because they did not
fit its rubric's idea of a conflict: both cases two independent labelers agreed on concerned the agents'
own work (duplicate tickets from parallel agents, an agent contradicting its own diagnosis), a category our
simulated benchmark does not contain. Some real conflicts would also need context beyond the chat, such as
ticket and tool state. This is where we would take the benchmark next."
