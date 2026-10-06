# proactive-memory-bench

A small benchmark for one question: **when an AI teammate sits in a team chat, does it notice on its own that a
new message conflicts with something said earlier**, and how does the way it stores chat history (its memory)
change that?

The hard case is the "I did" problem: the answer to a question is often a short reply like *"I'll take it"*,
*"nah hand it to me"* or a 👍 reaction, which shares no words with the question it answers. Memory that stores
messages one at a time loses who took what.

This is a one-week, rudimentary study, shared for discussion. Findings are in
[`results/findings.md`](results/findings.md); ideas for a next version are in
[`notes/real_data_lessons.md`](notes/real_data_lessons.md).

> ## ⚠️ Disclaimer: all chat data in this repo is fabricated
> The four simulated workspaces (`ando`, `anthropic`, `openai`, `xai`) are **fictional chats written by a language
> model**. Company names, product names and first names are used only as a familiar setting; every event, number,
> date, deal, person, decision and message is invented. Nothing here comes from, describes or represents any real
> company, team, conversation or person, and the project is not affiliated with or endorsed by any of the companies
> named. The separate real-data check (section 5) used a private dataset that is **not** included; only aggregate
> numbers are reported.

---

## 1. What is measured

At a decision point the agent sees the last 15 messages of the channel plus whatever its memory retrieves, and a
fixed judge (Claude Sonnet, fixed prompt and rubric) chooses one of:

- **INTERVENE**: the new message contradicts a team fact, quotes an outdated value, re-asks an answered question,
  or a check point has passed with the task undone;
- **TRACK**: it opens a commitment worth checking later;
- **IGNORE**: everything else (most messages).

Three layers are scored:

1. **Retrieval**: did all the evidence for the relevant fact reach the agent? *Proactive* = the agent queries with
   the latest messages, unprompted (the real use case); *reactive* = it is asked the question directly.
2. **Reader**: given what was retrieved, can a fixed reader answer the question?
3. **Decision**: does the judge INTERVENE on planted conflicts (within the next 2 messages), and how often does it
   raise false alarms?

## 2. Data

- 4 simulated workspaces, 876 messages, 21 threads, including Slack-style threads, interleaved side conversations
  and emoji reactions. Facts are stated in six **evidence forms**: explicit, ellipsis ("I'll take it"), reaction,
  correction, cross-reference, distributed.
- **303 decision points**: 36 planted conflicts (contradiction, stale quote, repeat question, missed deadline),
  13 commitments to track, 33 decoys (things that look like conflicts but aren't), 150 ordinary messages,
  71 follow-up messages.
- **155 probe triggers** (extra retrieval queries) and **142 paired conflict/control probes** (a wrong-value message
  and the same message with the correct value) to raise sample size.
- **Labels**: planted items carry their answer by construction. The other points were labeled by one human
  (100 + 32 rows, blind-adjudicated against the model) and a cross-family LLM labeler (GPT) for the remaining 171;
  see [`results/human_agreement.md`](results/human_agreement.md).

## 3. Memory strategies

5 ways of chunking chat × 3 retrievers = 15 strategies, each with a 1,500-token retrieval budget:

| Chunker | What one memory chunk is |
|---|---|
| A · per message | one message |
| B · window | 6 consecutive channel messages (stride 3) |
| C · reply-linked | a message plus up to two reply parents, inferred by Haiku (Cstar = the simulator's true links, as an upper bound) |
| D · topic segments | LLM-detected topic segments per channel |
| E · write-time rewrite | each message rewritten by Haiku into 0-2 standalone statements ("AJ took ownership of AND-341") |

Retrievers: BM25, embeddings (OpenAI `text-embedding-3-large`), hybrid (reciprocal rank fusion).
References: no memory (S0), true reply links (Cstar), two search-on-demand agents that grep the history with tools
(AG-grep, AG-both), and an oracle that is handed a perfect list of current facts and open items (OR).

## 4. Results

![15 memory strategies](results/figs/strategy_table.png)

*Retrieval*: % of queries (36 plants + 155 probe triggers) where all evidence reached the agent; *proactive* =
queried with the latest messages, *reactive* = asked the question directly. *Plants caught*: % of the 36 planted
conflicts where the judge intervened at the conflict or within 2 messages. *False alarms*: severity-weighted
INTERVENE on gold-IGNORE points per 100 decisions. Bold = best of the 15. Markdown version:
[`results/strategy_table.md`](results/strategy_table.md).

![Paired probes](results/figs/probe_table.png)

Paired probes run on the best-retriever cell of each chunker plus references. Markdown version:
[`results/probe_table.md`](results/probe_table.md).

### Headline findings

1. **Chunking decides what the agent sees.** Across the 15 strategies, retrieval varies 41 points by chunker and
   7 points by retriever (difference 35 pts, 95% CI 26-44, resampling by fact; holds with a second embedding
   model). Per-message memory delivers explicit facts 84% of the time but "I'll take it"-style answers 18%.
2. **Delivery predicts what the agent can know**: a reader answers correctly 93% of the time when the evidence
   was delivered, 3% when it was not.
3. **On the 36 natural plants, the strategies cannot be ranked**: 58-81% caught, intervals about ±15 pts, and
   rerunning the same judge moves cells by up to 8 pts. Any memory beats none (22%); the oracle catches 97%.
4. **On targeted wrong-value probes, more delivery means more catches**: rewrite memory (E1) catches 82% vs
   69% for windows and true reply links. This test was designed after seeing result 3 and covers only one
   conflict type; see the caveats in the findings.
5. **Missed deadlines are invisible to retrieval** (0-43% caught vs 100% for the oracle's open-item list);
   adding an open-item list to retrieved memory helps only half the time.
6. **More memory makes the judge speak more, not more accurately**: the oracle has the most false alarms;
   the grep agent, which searches only when needed, has the fewest.
7. **The judge model matters as much as the memory**: Haiku as judge catches 5-22 pts less with 2-3x the
   false alarms, and reorders the memory strategies.

## 5. Reality check on real chat

On 50 decision points from a real team where people and AI agents work together (private, not included), the same
judge **never intervened** (0/50, under Sonnet, Haiku and GPT, full or truncated thread). Two labelers each
flagged 5 cases but agreed on only 2, and both of those concern the agents' own work (duplicate tickets from
parallel agents, an agent contradicting its own diagnosis), a kind of conflict this benchmark does not simulate.
Aggregate numbers: [`results/real_check.md`](results/real_check.md); what the benchmark misses and ideas for a
next version: [`notes/real_data_lessons.md`](notes/real_data_lessons.md).

## 6. Limitations

- Simulated data from one model family; the judge is the same family. Four workspaces, 36 INTERVENE plants.
- Strategy differences at the decision level are within noise on natural plants; the paired probes are targeted.
- Conflicts are people changing facts; agent-made conflicts and tool state (tickets, deploys) are not modeled.
- Labels: one human plus an LLM labeler.
- About $80 of API calls in total (batch API for most judge runs).

## 7. Reproduce

```bash
uv sync
# Scoring and tables from the committed runs (no API keys needed):
uv run python -m eval.score            # results/main.csv, by_slice.csv, grid_stats.csv
uv run python -m eval.attribute        # why each plant was missed
uv run python -m eval.score_probes     # paired-probe decisions
uv run python -m eval.robustness       # second judge, second embedding model, rerun noise
uv run python -m eval.make_tables      # the tables and figure above
```

Regenerating anything with a model needs `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` in `.env`
(`SIM_MODEL`, `JUDGE_MODEL`, `CHEAP_JUDGE_MODEL`, `LABELER_MODEL`). In order: `sim.run_workspace` (generate
chats) → `world.verify` → `eval.select_points` → labeling (`label/`) → memory builds (`memory.linker`,
`memory.segment`, `memory.rewrite`) → `eval.retrieval_grid` and `eval.reader` → `judge.batch` / `judge.run` →
the scoring commands above. LLM responses are cached under `data/cache/` (not committed).

## 8. Repo layout

```
world/      fictional workspace ledgers (facts, plants, personas) + verify / stats / restatement audit
sim/        chat simulator and LLM client (disk-cached)
memory/     chunkers A-E, reply linker, topic segmenter, rewriter, retrievers, grep agent tools
probes/     probe triggers and paired conflict/control probes
judge/      fixed judge prompt, memory conditions, live and batch runners
label/      labeling sheets, LLM labeler, agreement and adjudication
eval/       decision-point selection, retrieval grid, reader, scoring, attribution, robustness, tables
data/       generated workspaces, decision points, gold labels, every judge run (data/real/ is private, ignored)
results/    all result tables, findings, figures
notes/      design notes and lessons for a next version
```
git add README.md eval/make_tables.py results/figs/strategy_table.png results/figs/probe_table.png results/*.md .gitignore
git commit -m "README: tables as images, drop duplicate markdown table"
git push





