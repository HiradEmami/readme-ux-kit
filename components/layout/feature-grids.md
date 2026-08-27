# Feature Grids

> Maturity: `stable`

Feature grids help readers understand the project shape quickly: capabilities, architecture, workflows, integrations, or guarantees. GitHub Markdown does not support responsive CSS grids, so use tables, compact cards, or section groups that render predictably.

Use grids after the hero and before long setup details.

## Three-Column Feature Grid

```markdown
## Features

| Capability | What it gives you | Best for |
| --- | --- | --- |
| Typed API | Clear contracts, editor help, safer refactors | Libraries and SDKs |
| Fast setup | One-command install and local startup | Developer tools |
| Production checks | Build, test, lint, and release workflows | Maintained projects |
```

## Card Grid With Icons

```markdown
## Features

|  |  |
| --- | --- |
| <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/dev/icon_cli.svg" width="28" alt=""> <br><strong>CLI first</strong><br>Run common workflows from predictable commands. | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/core/icon_shield_check.svg" width="28" alt=""> <br><strong>Production checks</strong><br>Validate configuration, tests, and release readiness. |
| <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/core/icon_docs.svg" width="28" alt=""> <br><strong>Documentation ready</strong><br>Copy polished README sections without building a docs site. | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/dev/icon_pipeline.svg" width="28" alt=""> <br><strong>Pipeline aware</strong><br>Expose build, deploy, and status signals where readers expect them. |
```

## Capability Matrix

```markdown
## Capability Matrix

| Area | Included | Notes |
| --- | :---: | --- |
| CLI workflow | Yes | Init, build, test, and release commands |
| TypeScript support | Yes | Types ship with the package |
| Docker support | Partial | Runtime image available, Compose optional |
| Observability | Yes | Health checks and structured logs |
| Cloud templates | Planned | Tracked in the roadmap |
```

## Product Feature Section

```markdown
## Why teams use it

| Outcome | Detail |
| --- | --- |
| Faster onboarding | New contributors can run the project with one documented path. |
| Cleaner releases | Build, test, version, and changelog workflows are visible from the README. |
| Better trust signals | Status badges, support matrix, and security links are easy to verify. |
| Lower maintenance | Reusable sections keep README updates small and consistent. |
```

## AI Feature Grid

```markdown
## System Capabilities

| Capability | Description | Artifact |
| --- | --- | --- |
| Dataset versioning | Every experiment points to a stable data snapshot. | `data/manifest.json` |
| Evaluation harness | Prompts, models, and metrics run through one repeatable flow. | `evals/` |
| Report generation | Summaries are exported for review and regression tracking. | `reports/` |
| Deployment path | Inference config is separated from experiment code. | `deploy/` |
```

## Visual Feature Band

```markdown
<p align="center">
  <img alt="Feature band" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/banners/particles/banner_network_particles.svg">
</p>

## Core Workflow

| Step | Purpose | Command |
| --- | --- | --- |
| Install | Prepare dependencies | `npm install` |
| Validate | Run checks | `npm test` |
| Build | Create production output | `npm run build` |
| Release | Publish versioned artifacts | `npm run release` |
```

## When To Use Each Pattern

| Pattern | Use when | Avoid when |
| --- | --- | --- |
| Simple table | Features are factual and short | Each item needs rich explanation |
| Icon cards | The README needs stronger visual hierarchy | The icons are decorative only |
| Capability matrix | Readers compare support levels | All rows are equally supported |
| Workflow table | The project has clear operating steps | Commands need long explanation |

## Design Rules

- Keep each cell short. Dense tables become hard to read on mobile.
- Use icons only when they clarify categories.
- Align feature names around outcomes, not internal implementation names.
- Keep the first feature row focused on the primary value proposition.
- Prefer two-column card tables over four-column tables for GitHub mobile rendering.

## Copy Checklist

- Replace placeholders and commands with real project behavior.
- Check that icons and banners exist before using raw URLs.
- Keep row labels parallel in length and tone.
- Preview tables on a narrow viewport.
