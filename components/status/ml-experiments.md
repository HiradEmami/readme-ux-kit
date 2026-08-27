# ML Experiments

> Maturity: `draft`

ML experiment sections make model work auditable. They should show what was tested, which data and metrics were used, what changed, and whether the result is ready for production or still exploratory.

Use this for model cards, research READMEs, benchmark repos, prompt experiments, fine-tuning projects, and evaluation harnesses.

## Experiment Summary

```markdown
## Experiment Status

| Experiment | Status | Dataset | Primary metric | Result |
| --- | --- | --- | --- | ---: |
| `baseline-v1` | ![Complete](https://img.shields.io/badge/complete-16a34a?style=flat-square) | `2026.05.0` | accuracy | `82.4%` |
| `retrieval-v2` | ![In review](https://img.shields.io/badge/in_review-f59e0b?style=flat-square) | `2026.05.0` | accuracy | `86.1%` |
| `reranker-v1` | ![Running](https://img.shields.io/badge/running-2563eb?style=flat-square) | `2026.05.0` | nDCG@10 | pending |
```

## Model Evaluation Panel

```markdown
## Evaluation

| Metric | Baseline | Current | Delta |
| --- | ---: | ---: | ---: |
| Accuracy | `82.4%` | `86.1%` | `+3.7` |
| F1 | `0.801` | `0.842` | `+0.041` |
| Latency p95 | `610ms` | `480ms` | `-130ms` |
| Cost per 1k requests | `$0.42` | `$0.36` | `-$0.06` |
```

## ML Badge Row

```markdown
[![Experiment](https://img.shields.io/badge/experiment-in_review-f59e0b?style=for-the-badge)](./reports)
[![Dataset](https://img.shields.io/badge/dataset-2026.05.0-2563eb?style=for-the-badge)](./data/manifest.json)
[![Eval](https://img.shields.io/badge/eval-regression_safe-16a34a?style=for-the-badge)](./evals)
[![Model](https://img.shields.io/badge/model-candidate-7c3aed?style=for-the-badge)](./models)
```

## AI System Header

```markdown
<p align="center">
  <img alt="Neural pulse divider" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/dividers/animated/lines/divider_neural_pulse.svg">
</p>
```

```markdown
<p align="center">
  <img alt="Brain activity icon" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/data-ai/Icon_brain_activity.svg" width="72">
</p>
```

## Run An Experiment

````markdown
## Run Evaluation

```bash
python -m evals.run \
  --config evals/configs/retrieval-v2.yaml \
  --dataset data/manifest.json \
  --output reports/retrieval-v2.json
```

```text
experiment: retrieval-v2
dataset: 2026.05.0
status: complete
accuracy: 0.861
f1: 0.842
```
````

## Decision Log

```markdown
## Experiment Decision

| Field | Value |
| --- | --- |
| Decision | Promote `retrieval-v2` to candidate |
| Reason | Improves accuracy and F1 while reducing p95 latency |
| Risk | Needs additional evaluation on non-English samples |
| Follow-up | Add multilingual slice eval before production rollout |
| Owner | `@team-ml-platform` |
```

## Error Analysis

```markdown
## Error Analysis

| Slice | Failure mode | Next action |
| --- | --- | --- |
| Long context | Misses late evidence | Add retrieval window ablation |
| Ambiguous labels | Overconfident classification | Review label guide and confidence threshold |
| Non-English | Lower recall | Add language-specific eval slices |
```

## Model Card Snapshot

```markdown
## Model Snapshot

| Field | Value |
| --- | --- |
| Model | `retrieval-v2` |
| Dataset | `2026.05.0` |
| Intended use | Assisted search and summarization |
| Not intended for | Legal, medical, or safety-critical decisions |
| Monitoring | Latency, rejection rate, accuracy sample audits |
| Rollback | `baseline-v1` |
```

## Design Rules

- Include dataset version with every experiment result.
- Report at least one quality metric and one operational metric.
- Separate "running", "candidate", and "production" status.
- Document negative results when they affect future work.
- Avoid leaderboard-style claims without reproducible commands and data references.

## Copy Checklist

- Replace metrics with real evaluation outputs.
- Link reports, configs, datasets, and model artifacts.
- Identify the owner or reviewer for candidate experiments.
- Remove or mark stale experiments clearly.
