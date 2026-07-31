# Design Maturity

Design maturity helps users choose snippets based on reliability and polish level.

## Markers

| Marker | Meaning | Use when |
| --- | --- | --- |
| `stable` | Ready for broad reuse with normal placeholder replacement. | The snippet is GitHub-compatible, well-structured, and unlikely to need redesign before use. |
| `draft` | Useful and copyable, but still evolving. | The snippet works, but wording, density, or composition may need closer project-specific editing. |
| `experimental` | High-expression or advanced pattern. | The snippet is intentionally bolder, motion-heavy, or dependent on careful visual review. |

## Review Rules

- Prefer `stable` for templates and components that can be copied into most repositories safely.
- Use `draft` when the pattern is useful but still needs more real-world examples or polish.
- Use `experimental` for expressive badge sets, animated hero patterns, or generated visuals that may not fit conservative repositories.
- Do not mark a component `stable` until it uses GitHub-compatible Markdown/HTML and has clear customization notes.
- Revisit maturity when a component gets substantially rewritten.

## Template Maturity

| Template | Maturity | Reason |
| --- | --- | --- |
| [`templates/minimal.md`](../templates/minimal.md) | `stable` | Small, generic structure with low visual risk. |
| [`templates/backend-service.md`](../templates/backend-service.md) | `stable` | Operational sections are practical and easy to verify. |
| [`templates/open-source-lib.md`](../templates/open-source-lib.md) | `stable` | Covers common library README needs with predictable sections. |
| [`templates/ml-project.md`](../templates/ml-project.md) | `draft` | ML claims and artifacts require project-specific validation. |
| [`templates/research-project.md`](../templates/research-project.md) | `draft` | Research READMEs vary heavily by paper, dataset, and reproducibility scope. |

## Component Maturity

| Component | Maturity | Reason |
| --- | --- | --- |
| [`components/badges/system-badges.md`](../components/badges/system-badges.md) | `stable` | Factual, restrained, and broadly reusable. |
| [`components/badges/animated-badges.md`](../components/badges/animated-badges.md) | `draft` | Useful, but motion should be used selectively. |
| [`components/badges/neon-badges.md`](../components/badges/neon-badges.md) | `experimental` | High-expression visual style that needs project fit review. |
| [`components/interactive/expand-collapse.md`](../components/interactive/expand-collapse.md) | `stable` | Native GitHub-supported disclosure pattern. |
| [`components/interactive/tabs.md`](../components/interactive/tabs.md) | `draft` | Tab-like patterns need careful heading and anchor maintenance. |
| [`components/interactive/terminal-blocks.md`](../components/interactive/terminal-blocks.md) | `stable` | Searchable, copyable, and reliable across GitHub rendering. |
| [`components/interactive/typing-headers.md`](../components/interactive/typing-headers.md) | `experimental` | Animated hero usage needs visual and accessibility review. |
| [`components/layout/faq.md`](../components/layout/faq.md) | `stable` | Low-risk structure that improves scanning. |
| [`components/layout/feature-grids.md`](../components/layout/feature-grids.md) | `stable` | Table-based layout works predictably in GitHub Markdown. |
| [`components/layout/hero-sections.md`](../components/layout/hero-sections.md) | `draft` | Hero composition depends strongly on project tone and asset choice. |
| [`components/layout/roadmap.md`](../components/layout/roadmap.md) | `draft` | Roadmaps need careful wording to avoid overpromising. |
| [`components/status/dataset-status.md`](../components/status/dataset-status.md) | `draft` | Dataset claims require real provenance and maintenance. |
| [`components/status/deployment-status.md`](../components/status/deployment-status.md) | `stable` | Operational tables are clear when values are real. |
| [`components/status/ml-experiments.md`](../components/status/ml-experiments.md) | `draft` | Experiment status must be adapted to real metrics and artifacts. |
| [`components/status/version-lifecycle.md`](../components/status/version-lifecycle.md) | `stable` | Lifecycle tables are broadly reusable and easy to verify. |
