# Dataset Status

> Maturity: `draft`

Dataset status sections help readers trust the data behind a project. They show version, freshness, license, quality checks, lineage, and known limitations without burying the README in data documentation.

Use this for ML projects, analytics repositories, benchmark suites, data pipelines, research projects, and public datasets.

## Dataset Overview

```markdown
## Dataset Status

| Dataset | Version | Rows | Updated | License |
| --- | --- | ---: | --- | --- |
| `training` | `2026.05.0` | `1,240,000` | `2026-05-02` | `CC-BY-4.0` |
| `validation` | `2026.05.0` | `80,000` | `2026-05-02` | `CC-BY-4.0` |
| `test` | `2026.05.0` | `80,000` | `2026-05-02` | restricted |
```


## Data Quality Panel

```markdown
## Data Quality

| Check | Status | Threshold | Current |
| --- | --- | ---: | ---: |
| Schema validation | ![Passing](https://img.shields.io/badge/passing-16a34a?style=flat-square) | `100%` | `100%` |
| Missing values | ![Passing](https://img.shields.io/badge/passing-16a34a?style=flat-square) | `< 1%` | `0.24%` |
| Duplicate records | ![Review](https://img.shields.io/badge/review-f59e0b?style=flat-square) | `< 0.5%` | `0.61%` |
| Label coverage | ![Passing](https://img.shields.io/badge/passing-16a34a?style=flat-square) | `> 98%` | `99.2%` |
```

## Dataset Badge Row

```markdown
[![Dataset](https://img.shields.io/badge/dataset-versioned-2563eb?style=for-the-badge)](./data)
[![Schema](https://img.shields.io/badge/schema-validated-16a34a?style=for-the-badge)](./data/schema.json)
[![License](https://img.shields.io/badge/license-CC--BY--4.0-475569?style=for-the-badge)](./LICENSE)
[![Freshness](https://img.shields.io/badge/updated-2026--05--02-0f766e?style=for-the-badge)](./data/manifest.json)
```

## Data Pipeline Header

```markdown
<p align="center">
  <img alt="Data pipeline icon" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/data-ai/icon_data_pipeline.svg" width="72">
</p>

## Data Pipeline

| Stage | Artifact | Owner |
| --- | --- | --- |
| Ingest | `data/raw/` | Data engineering |
| Validate | `reports/quality/` | ML platform |
| Transform | `data/processed/` | Research |
| Publish | `data/manifest.json` | Maintainers |
```

## Manifest Example

````markdown
## Dataset Manifest

```json
{
  "name": "example-dataset",
  "version": "2026.05.0",
  "created_at": "2026-05-02",
  "splits": {
    "train": 1240000,
    "validation": 80000,
    "test": 80000
  },
  "schema": "data/schema.json",
  "license": "CC-BY-4.0"
}
```
````

## Known Limitations

```markdown
## Dataset Limitations

- The test split is not redistributed to prevent benchmark leakage.
- Records before `2024-01-01` may have weaker metadata coverage.
- Non-English samples are underrepresented and should be evaluated separately.
- Labels are reviewed by two annotators for high-impact categories and one annotator elsewhere.
```

## Reproducibility Block

````markdown
## Reproduce The Dataset

```bash
python scripts/download_data.py --version 2026.05.0
python scripts/validate_data.py --manifest data/manifest.json
python scripts/build_splits.py --seed 42
```

Expected outputs:

```text
data/raw/
data/processed/
data/manifest.json
reports/quality/summary.json
```
````

## Design Rules

- Always include version, update date, and license.
- Separate data quality from model quality. They answer different trust questions.
- Use exact split sizes when possible.
- Document known limitations plainly.
- Link to the manifest, schema, data card, or pipeline scripts when they exist.

## Copy Checklist

- Replace sample counts, dates, paths, and licenses.
- Confirm whether test data can be public.
- Keep dataset status synced with experiment reports.
- Avoid vague claims like "clean data" without checks or thresholds.
