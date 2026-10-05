# Label quality: one human + a cross-family LLM labeler

Labels for all 303 decision points are in `data/gold/labels.json` (each tagged with its source).

| Points | Source |
|---|---|
| 100 overlap (50 triggers + 50 ordinary) | human first pass, then blind adjudication against the model |
| 32 triggers_rest | human first pass, then blind adjudication against the model |
| 171 ordinary_rest (100 ordinary + 71 after-trigger) | LLM labeler only (gpt-6-luna, prompt v2) |

Final label mix: IGNORE 214, TRACK 51, INTERVENE 38.

## Labeler
- Model: `gpt-6-luna` (OpenAI; different family from the Claude simulator and judge).
- Prompt: rubric v1 + a 6-step procedure (`label/llm_label.py`, `v2`). v1 → v2 was tuned on the
  30-row dev split only: judge the decision message only; fire an overdue item only at the first
  message after its check point; TRACK needs an explicit check point.
- Test split (70 overlap rows) was run once, after the prompt was frozen.

## Agreement

| Comparison | Rows | Raw | κ (3-class) | κ (INTERVENE vs not) |
|---|---|---|---|---|
| Human first pass vs model, overlap test | 70 | 0.76 | 0.59 | 0.76 |
| Human first pass vs model, overlap all | 100 | 0.72 | 0.48 | 0.56 |
| Human first pass vs model, triggers_rest | 32 | 0.66 | 0.46 | 0.43 |
| Adjudicated vs model, overlap test | 70 | 0.99 | 0.98 | 1.00 |
| Adjudicated vs model, overlap all | 100 | 0.96 | 0.93 | 0.94 |
| Adjudicated vs model, triggers_rest | 32 | 0.91 | 0.85 | 0.93 |
| Human vs human (blind relabel, ~1 day later) | 30 | 0.97 | 0.94 | — |

## Accuracy on planted labels (independent of any labeler)

| Labeler | Overlap (50) | Triggers_rest (32) | Total (82) |
|---|---|---|---|
| Human first pass | 33 | 21 | 54 (66%) |
| Model | 44 | 30 | 74 (90%) |
| Human adjudicated | 47 | 29 | 76 (93%) |

## Caveats
- **Adjudicated κ is an upper bound.** Adjudication only revisited disagreement rows, and the
  model's label was one of the two (unattributed) candidates. The human sided with the model on
  24/28 overlap and 8/11 triggers_rest disagreements.
- **Intra-rater κ is inflated.** The 30 relabel rows were drawn from rows *not* revisited during
  adjudication, which are exactly the rows where human and model already agreed, i.e. the easier
  ones. So 0.94 measures consistency on easy rows, not on the hard ones.
- **Reliability ≠ validity.** The human was consistent with himself but missed about a third of
  the planted conflicts on the first pass; errors were almost all misses (labeling a real conflict
  IGNORE), not false alarms. The planted-label accuracy is therefore the main evidence that the
  model is a valid labeler; κ against the human first pass understates it.

## Decision
Use the model's labels for the 171 points no human labeled. The original acceptance rule
(model κ ≥ intra-rater κ − 0.05) is not meaningful here for the two reasons above; the deciding
evidence is planted-label accuracy (model 90% vs human first pass 66%) and κ 0.85–0.93 against
adjudicated labels.

## Finding worth reporting
A careful human reading each decision point with the team facts on screen missed 34% of the
planted conflicts. This is the failure the benchmark targets: the conflicting fact is present
but far from the message, and nothing points to it.
