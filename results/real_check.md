# Real-data check (aggregate only; the data is private)

50 decision points from 10 real team-chat conversations between people and AI agents. Each case is
one thread plus a new message, so this checks the judge on real chat; no cross-thread retrieval is involved.
Same judge prompt and rubric as the benchmark.

## Reference labels
- Claude first pass: 5/50 should intervene; GPT labeler (gpt-6-luna): 5/50.
- Agreement 88%, kappa 0.33: they agree on 2 positives (conflict-candidate-005, conflict-candidate-023); 6 more are flagged by only one.
- Consensus reference = cases where both labelers agree (disputed cases excluded).

## Judge on real chat

| condition   |   n |   INTERVENE |   TRACK | catch_vs_consensus   | false_alarm_vs_consensus   | catch_vs_claude   | false_alarm_vs_claude   | catch_vs_gpt   | false_alarm_vs_gpt   |
|:------------|----:|------------:|--------:|:---------------------|:---------------------------|:------------------|:------------------------|:---------------|:---------------------|
| FULL        |  50 |           0 |       2 | 0/2                  | 0/42 (0%)                  | 0/5               | 0/45 (0%)               | 0/5            | 0/45 (0%)            |
| FULL~gpt    |  50 |           0 |       0 | 0/2                  | 0/42 (0%)                  | 0/5               | 0/45 (0%)               | 0/5            | 0/45 (0%)            |
| FULL~haiku  |  50 |           0 |       8 | 0/2                  | 0/42 (0%)                  | 0/5               | 0/45 (0%)               | 0/5            | 0/45 (0%)            |
| LAST15      |  50 |           0 |       2 | 0/2                  | 0/42 (0%)                  | 0/5               | 0/45 (0%)               | 0/5            | 0/45 (0%)            |

FULL = whole thread shown; LAST15 = last 15 messages only; ~haiku / ~gpt = different judge model.
catch = INTERVENE on reference-positive cases; false_alarm = INTERVENE on reference-negative cases.
TRACK given on: {'FULL': 2, 'FULL~haiku': 8, 'LAST15': 2}.

## Findings
1. Real conflicts are ambiguous: two independent model labelers each mark about 10% of cases, but agree on only 2 (kappa 0.33), versus clean planted conflicts in the simulation.
2. The judge intervened on 0 of 50 cases under every condition (Sonnet, Haiku, GPT; full or truncated thread): no false alarms, and it missed both consensus conflicts. A judge tuned for fact conflicts stays silent on these.
3. The candidate conflicts concern the agents' own claims and work (promising actions they cannot take, contradicting their own earlier diagnosis, duplicate tickets from parallel agents), a category the simulated benchmark (people changing dates, owners and numbers) does not cover.

