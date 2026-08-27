# Components

Reusable Markdown sections for building GitHub-native READMEs. Components should be copied into a README and customized for the target project.

| Group | Purpose | Maturity range |
| --- | --- | --- |
| [Badges](./badges/) | Build status, release, package, security, and system signal rows. | `stable` to `experimental` |
| [Interactive](./interactive/) | GitHub-compatible collapsible sections, tab-like details, terminal blocks, and typing headers. | `stable` to `experimental` |
| [Layout](./layout/) | Hero sections, feature grids, FAQs, and roadmaps. | `stable` to `draft` |
| [Status](./status/) | Deployment, dataset, experiment, and version lifecycle sections. | `stable` to `draft` |

## Maturity

Use the maturity marker to decide how much review a component needs before copying it.

| Marker | Meaning |
| --- | --- |
| `stable` | Ready for broad reuse after normal placeholder replacement. |
| `draft` | Useful and copyable, but still needs closer project-specific editing. |
| `experimental` | High-expression or advanced pattern that needs visual and accessibility review. |

For the full maturity policy, see [Design maturity](../docs/MATURITY.md).

## Component Index

| Component | Maturity | Best for |
| --- | --- | --- |
| [System badges](./badges/system-badges.md) | `stable` | Factual release, build, package, and security signals. |
| [Animated badges](./badges/animated-badges.md) | `draft` | Motion-accented status rows used sparingly. |
| [Neon badges](./badges/neon-badges.md) | `experimental` | High-energy demos, AI projects, and portfolio repos. |
| [Expand and collapse](./interactive/expand-collapse.md) | `stable` | Advanced details, troubleshooting, and long examples. |
| [Tabs](./interactive/tabs.md) | `draft` | GitHub-compatible tab-like navigation with anchors. |
| [Terminal blocks](./interactive/terminal-blocks.md) | `stable` | Install, quick start, CLI, deploy, and troubleshooting commands. |
| [Typing headers](./interactive/typing-headers.md) | `experimental` | Animated hero headers and generated typing SVGs. |
| [FAQ](./layout/faq.md) | `stable` | Scope, support, installation, and licensing questions. |
| [Feature grids](./layout/feature-grids.md) | `stable` | Capability tables and compact project summaries. |
| [Hero sections](./layout/hero-sections.md) | `draft` | First-screen README composition. |
| [Roadmap](./layout/roadmap.md) | `draft` | Direction, milestones, and planned work. |
| [Dataset status](./status/dataset-status.md) | `draft` | Dataset freshness, quality, and provenance. |
| [Deployment status](./status/deployment-status.md) | `stable` | Production, staging, uptime, and runbook signals. |
| [ML experiments](./status/ml-experiments.md) | `draft` | Experiment tracking, metrics, and model status. |
| [Version lifecycle](./status/version-lifecycle.md) | `stable` | Supported versions, migration, and maintenance windows. |

## Copy Checklist

- Replace placeholders.
- Keep links verifiable.
- Keep badge rows short.
- Prefer GitHub-compatible Markdown and HTML.
- Avoid custom JavaScript or external CSS.
