# README Recipes

Recipes are complete assembly plans: start with one template, apply one theme, add a small set of components, and choose assets that reinforce the project type.

Use these when you want a polished README quickly without browsing every asset category first.

For paste-ready complete starters, use [Copy-all README bundles](./BUNDLES.md).

## Open-Source Library README

Best for packages, SDKs, utilities, and reusable modules.

### Ingredients

| Layer | Use |
| --- | --- |
| Template | [`templates/open-source-lib.md`](../templates/open-source-lib.md) |
| Theme | [`themes/minimal/example.md`](../themes/minimal/example.md) |
| Badges | [`components/badges/system-badges.md`](../components/badges/system-badges.md) |
| Layout | [`components/layout/feature-grids.md`](../components/layout/feature-grids.md) |
| Status | [`components/status/version-lifecycle.md`](../components/status/version-lifecycle.md) |

### Recommended Assets

- [`assets/headers/static/header_minimal_lux.svg`](../assets/headers/static/header_minimal_lux.svg)
- [`assets/dividers/static/divider_minimal_clean.svg`](../assets/dividers/static/divider_minimal_clean.svg)
- [`assets/icons/dev/icon_package_box.svg`](../assets/icons/dev/icon_package_box.svg)
- [`assets/icons/core/icon_docs.svg`](../assets/icons/core/icon_docs.svg)

### Assembly Order

1. Copy the open-source library template.
2. Add the minimal header and a compact badge row.
3. Keep installation and quick start above the fold.
4. Add API examples before architecture details.
5. Put compatibility, testing, versioning, and security near the bottom.

## Machine Learning Project README

Best for model repos, evaluation suites, notebooks, datasets, and inference workflows.

### Ingredients

| Layer | Use |
| --- | --- |
| Template | [`templates/ml-project.md`](../templates/ml-project.md) |
| Theme | [`themes/ai-neural/example.md`](../themes/ai-neural/example.md) |
| Status | [`components/status/ml-experiments.md`](../components/status/ml-experiments.md) |
| Status | [`components/status/dataset-status.md`](../components/status/dataset-status.md) |
| Layout | [`components/layout/roadmap.md`](../components/layout/roadmap.md) |

### Recommended Assets

- [`assets/headers/animated/header_radial_core.svg`](../assets/headers/animated/header_radial_core.svg)
- [`assets/visuals/evaluation_lens_matrix.svg`](../assets/visuals/evaluation_lens_matrix.svg)
- [`assets/visuals/model_release_constellation.svg`](../assets/visuals/model_release_constellation.svg)
- [`assets/icons/data-ai/icon_eval_harness.svg`](../assets/icons/data-ai/icon_eval_harness.svg)

### Assembly Order

1. Start with the ML project template.
2. Put the task, dataset, metric, and current best result in the first table.
3. Add dataset status before training instructions.
4. Add evaluation commands and expected artifacts.
5. Include model card, limitations, and reproducibility metadata.

## Backend Service README

Best for APIs, workers, internal services, platform components, and production systems.

### Ingredients

| Layer | Use |
| --- | --- |
| Template | [`templates/backend-service.md`](../templates/backend-service.md) |
| Theme | [`themes/terminal/example.md`](../themes/terminal/example.md) or [`themes/cyberpunk/example.md`](../themes/cyberpunk/example.md) |
| Status | [`components/status/deployment-status.md`](../components/status/deployment-status.md) |
| Interactive | [`components/interactive/terminal-blocks.md`](../components/interactive/terminal-blocks.md) |
| Layout | [`components/layout/faq.md`](../components/layout/faq.md) |

### Recommended Assets

- [`assets/headers/static/header_data_rail.svg`](../assets/headers/static/header_data_rail.svg)
- [`assets/visuals/reliability_control_room.svg`](../assets/visuals/reliability_control_room.svg)
- [`assets/icons/devops/icon_observability_scope.svg`](../assets/icons/devops/icon_observability_scope.svg)
- [`assets/dividers/animated/bars/divider_circuit_pulse_bar.svg`](../assets/dividers/animated/bars/divider_circuit_pulse_bar.svg)

### Assembly Order

1. Start with service purpose, ownership boundaries, and architecture.
2. Show health and primary endpoints early.
3. Add local development and configuration tables.
4. Add deployment status, SLOs, alerts, and runbook guidance.
5. Keep operations factual and easy to scan during incidents.

## GitHub Profile README

Best for personal profile READMEs, portfolio pages, and author introductions.

### Ingredients

| Layer | Use |
| --- | --- |
| Template | [`templates/minimal.md`](../templates/minimal.md) |
| Theme | [`themes/minimal/example.md`](../themes/minimal/example.md) |
| Layout | [`components/layout/hero-sections.md`](../components/layout/hero-sections.md) |
| Layout | [`components/layout/feature-grids.md`](../components/layout/feature-grids.md) |
| Interactive | [`components/interactive/expand-collapse.md`](../components/interactive/expand-collapse.md) |

### Recommended Assets

- [`assets/personal/four_pillars.svg`](../assets/personal/four_pillars.svg)
- [`assets/personal/traditional_vs_engineered.svg`](../assets/personal/traditional_vs_engineered.svg)
- [`assets/visuals/collaboration.svg`](../assets/visuals/collaboration.svg)
- [`assets/icons/objects/icon_rocket_launch.svg`](../assets/icons/objects/icon_rocket_launch.svg)

### Assembly Order

1. Use a short hero with your name, role, and current focus.
2. Add three to five pillars instead of a long autobiography.
3. Show selected work with compact cards or tables.
4. Put contact links and current availability near the top or bottom.
5. Keep animation subtle so the page still feels professional.

## Security-Focused Repository README

Best for security tools, audit utilities, policy repos, scanners, and incident-response projects.

### Ingredients

| Layer | Use |
| --- | --- |
| Template | [`templates/backend-service.md`](../templates/backend-service.md) or [`templates/open-source-lib.md`](../templates/open-source-lib.md) |
| Theme | [`themes/cyberpunk/example.md`](../themes/cyberpunk/example.md) |
| Badges | [`components/badges/system-badges.md`](../components/badges/system-badges.md) |
| Status | [`components/status/deployment-status.md`](../components/status/deployment-status.md) |
| Interactive | [`components/interactive/expand-collapse.md`](../components/interactive/expand-collapse.md) |

### Recommended Assets

- [`assets/file_headers/security_policy_radar.svg`](../assets/file_headers/security_policy_radar.svg)
- [`assets/visuals/privacy_vault_shield.svg`](../assets/visuals/privacy_vault_shield.svg)
- [`assets/icons/status/icon_warning.svg`](../assets/icons/status/icon_warning.svg)
- [`assets/dividers/animated/lines/divider_red_alert.svg`](../assets/dividers/animated/lines/divider_red_alert.svg)

### Assembly Order

1. State scope and threat model clearly.
2. Put install and safe usage instructions before advanced configuration.
3. Document supported inputs, outputs, and limitations.
4. Include security reporting instructions.
5. Use warning and danger visuals only for real risk signals.

## Final Check

After assembling a README from any recipe:

```bash
npm run check:all
```

Then preview the rendered README on GitHub before publishing.
