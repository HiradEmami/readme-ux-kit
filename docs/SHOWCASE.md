# Community Showcase

This page tracks real repositories using `readme-ux-kit` assets, templates, themes, or components.

The showcase is intentionally curated. Entries should help future users understand what the kit looks like in real README pages, not just list every repository that copied one SVG.

## Featured Examples

No community entries have been accepted yet.

To add one, open a pull request that updates this file and follows the submission rules below.

## Reference Examples

These examples are not external community repositories. They are curated composition patterns that show how the kit can be used in real README situations while the public showcase waits for accepted submissions.

### Polished Open-Source Library

| Field | Details |
| --- | --- |
| Project type | Open-source library or SDK |
| Kit pieces used | [`templates/open-source-lib.md`](../templates/open-source-lib.md), [`themes/open-source-classic/example.md`](../themes/open-source-classic/example.md), [`components/status/version-lifecycle.md`](../components/status/version-lifecycle.md) |
| Recommended assets | [`header_hero_banner.svg`](../assets/headers/static/header_hero_banner.svg), [`divider_center_diamond.svg`](../assets/dividers/static/divider_center_diamond.svg), [`icon_pull_request.svg`](../assets/icons/dev/icon_pull_request.svg) |
| Good example of | Familiar project introduction, contributor path, support expectations |

Use this pattern when a repository needs to feel approachable without becoming decorative. The README should answer what the package does, how to install it, what version is supported, and how contributors can help.

```markdown
[![Open source header](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_hero_banner.svg)](https://github.com/HiradEmami/readme-ux-kit)

## Project Basics

| Topic | Answer |
| --- | --- |
| What is it? | A practical package that solves one clear problem. |
| How stable is it? | Maintained with semantic releases. |
| How to help? | Issues, docs, and focused pull requests. |
```

### Production Backend Service

| Field | Details |
| --- | --- |
| Project type | Backend service, platform API, or internal production system |
| Kit pieces used | [`templates/backend-service.md`](../templates/backend-service.md), [`themes/enterprise/example.md`](../themes/enterprise/example.md), [`components/status/deployment-status.md`](../components/status/deployment-status.md) |
| Recommended assets | [`header_status_dashboard.svg`](../assets/headers/static/header_status_dashboard.svg), [`reliability_control_room.svg`](../assets/visuals/reliability_control_room.svg), [`icon_slo_gauge.svg`](../assets/icons/devops/icon_slo_gauge.svg) |
| Good example of | Production posture, ownership, support model, operational confidence |

Use this pattern when readers need to know whether a service is stable, supported, observable, and safe to depend on. It works best with short status tables and explicit ownership metadata.

```markdown
[![Enterprise header](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_status_dashboard.svg)](https://github.com/HiradEmami/readme-ux-kit)

## Production Snapshot

| Signal | Current | Owner |
| --- | --- | --- |
| Release channel | Stable | Platform |
| Security posture | Reviewed | AppSec |
```

### Model or Data Research Repo

| Field | Details |
| --- | --- |
| Project type | ML project, benchmark suite, dataset, or experiment repository |
| Kit pieces used | [`templates/ml-project.md`](../templates/ml-project.md), [`templates/research-project.md`](../templates/research-project.md), [`themes/data-lab/example.md`](../themes/data-lab/example.md), [`components/status/ml-experiments.md`](../components/status/ml-experiments.md) |
| Recommended assets | [`header_data_rail.svg`](../assets/headers/static/header_data_rail.svg), [`data_lineage_river.svg`](../assets/visuals/data_lineage_river.svg), [`divider_data_flow.svg`](../assets/dividers/animated/lines/divider_data_flow.svg) |
| Good example of | Dataset status, experiment decisions, benchmark context |

Use this pattern when the README needs to make evidence easy to inspect. Prefer tables that include split, baseline, current metric, and decision instead of isolated performance claims.

```markdown
[![Data lab header](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_data_rail.svg)](https://github.com/HiradEmami/readme-ux-kit)

## Experiment Ledger

| Run | Change | Metric | Decision |
| --- | --- | --- | --- |
| `exp-041` | Added temporal features | +3.1% AUC | Keep |
```

### Security Tool or Policy Repo

| Field | Details |
| --- | --- |
| Project type | Scanner, security workflow, policy engine, or disclosure-focused repository |
| Kit pieces used | [`themes/security-ops/example.md`](../themes/security-ops/example.md), [`components/badges/system-badges.md`](../components/badges/system-badges.md), [`components/interactive/expand-collapse.md`](../components/interactive/expand-collapse.md) |
| Recommended assets | [`security_policy_radar.svg`](../assets/file_headers/security_policy_radar.svg), [`privacy_vault_shield.svg`](../assets/visuals/privacy_vault_shield.svg), [`divider_scanning_radar.svg`](../assets/dividers/animated/lines/divider_scanning_radar.svg) |
| Good example of | Trust boundaries, required checks, disclosure clarity |

Use this pattern when the README must help readers understand what is checked, what is not checked, and how risk is handled. Keep alert visuals meaningful and avoid using red for ordinary status.

```markdown
[![Security ops header](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/file_headers/security_policy_radar.svg)](https://github.com/HiradEmami/readme-ux-kit)

## Control Plane

| Control | Status | Evidence |
| --- | --- | --- |
| Dependency scan | Required | CI gate |
```

### Documentation Site or API Reference

| Field | Details |
| --- | --- |
| Project type | Documentation site, API reference, SDK guide, or examples repository |
| Kit pieces used | [`themes/docs-clean/example.md`](../themes/docs-clean/example.md), [`components/interactive/tabs.md`](../components/interactive/tabs.md), [`components/layout/faq.md`](../components/layout/faq.md) |
| Recommended assets | [`header_split_line.svg`](../assets/headers/static/header_split_line.svg), [`icon_docs.svg`](../assets/icons/core/icon_docs.svg), [`icon_breadcrumb_path.svg`](../assets/icons/navigation/icon_breadcrumb_path.svg) |
| Good example of | Fast navigation, clean reference structure, low-noise examples |

Use this pattern when the README acts as a front door for deeper docs. The strongest version starts with a route table and keeps examples close to the API concepts they explain.

```markdown
[![Docs clean header](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_split_line.svg)](https://github.com/HiradEmami/readme-ux-kit)

## Start Here

| Need | Go to |
| --- | --- |
| Install | Quick start |
| Learn API | Reference |
```

## Submission Rules

Add a repository only when it meets all of these checks:

- The repository is public and safe to link from this project.
- The README or documentation visibly uses at least one asset, template, theme, or component from this kit.
- The project owner is comfortable being listed.
- The entry explains what was used and why it is a useful example.
- The repository does not use this kit in a misleading, abusive, or spammy context.

## Entry Format

Use this format for each accepted showcase entry:

```markdown
### Repository Name

| Field | Details |
| --- | --- |
| Repository | [owner/repo](https://github.com/owner/repo) |
| Project type | Open-source library, backend service, ML project, profile README, docs site, or other |
| Kit pieces used | Assets, template, theme, components, or generated SVG |
| Good example of | Hero section, status area, project navigation, visual identity, profile storytelling, or another specific pattern |

Short note explaining why the README is useful as a reference.
```

## What To Highlight

Good showcase entries call out specific reusable patterns:

| Pattern | What to mention |
| --- | --- |
| Hero section | Which banner, header, theme, or layout creates the first impression. |
| Asset composition | Which assets work well together without visual noise. |
| Status design | How badges, loaders, progress bars, or lifecycle sections make project state easier to scan. |
| Template adaptation | How a starter template was customized for a real project. |
| Accessibility | How the README remains readable in GitHub light and dark mode. |
| Reader journey | How the README moves from overview to setup, usage, trust, and contribution. |
| Copy surface | Which snippets, tables, or bundles are easiest for another maintainer to reuse. |

## Review Checklist

Before accepting a showcase entry, reviewers should confirm:

- Links work and point to the intended public repository.
- The repository actually uses this kit or clearly credits an adapted snippet.
- The entry is concise and does not read like an advertisement.
- The example teaches a useful README pattern.
- The entry follows the table format above.

## Starter Queue

Use this section for proposed entries that need review or owner confirmation.

| Repository | Status | Notes |
| --- | --- | --- |
| _None yet_ | Pending | Add candidates through a pull request. |
