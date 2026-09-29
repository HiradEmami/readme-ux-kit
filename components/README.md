# Components

Reusable Markdown sections for building GitHub-native READMEs. Components should be copied into a README and customized for the target project.

## Component Groups

| Group | Purpose |
| --- | --- |
| [Adoption](./adoption/) | Adoption components for complete README composition. |
| [Badges](./badges/) | Existing component family. |
| [Community](./community/) | Community components for complete README composition. |
| [Interactive](./interactive/) | Existing component family. |
| [Layout](./layout/) | Existing component family. |
| [Navigation](./navigation/) | Navigation components for complete README composition. |
| [Onboarding](./onboarding/) | Onboarding components for complete README composition. |
| [Quality](./quality/) | Quality components for complete README composition. |
| [Reference](./reference/) | Reference components for complete README composition. |
| [Release](./release/) | Release components for complete README composition. |
| [Status](./status/) | Existing component family. |
| [Trust](./trust/) | Trust components for complete README composition. |

## Maturity

| Marker | Meaning |
| --- | --- |
| `stable` | Ready for broad reuse after normal placeholder replacement. |
| `draft` | Useful and copyable, but still needs closer project-specific editing. |
| `experimental` | High-expression or advanced pattern that needs visual and accessibility review. |

For the full maturity policy, see [Design maturity](../docs/MATURITY.md).

## Component Index

| Component | Maturity | Best for |
| --- | --- | --- |
| [Case Study](./adoption/case-study.md) | `draft` | Short implementation story with measurable outcome. |
| [Comparison Table](./adoption/comparison-table.md) | `draft` | Transparent feature comparison without fake claims. |
| [Decision Matrix](./adoption/decision-matrix.md) | `stable` | When to use, avoid, or compare against alternatives. |
| [Use Cases](./adoption/use-cases.md) | `stable` | Clear use cases and non-goals for product fit. |
| [Animated badges](./badges/animated-badges.md) | `draft` | Motion-accented status rows used sparingly. |
| [Neon badges](./badges/neon-badges.md) | `experimental` | High-energy demos, AI projects, and portfolio repos. |
| [System badges](./badges/system-badges.md) | `stable` | Factual release, build, package, and security signals. |
| [Contributor Journey](./community/contributor-journey.md) | `stable` | Issue selection, local setup, review, and release path. |
| [Funding](./community/funding.md) | `draft` | Sponsorship, support tiers, and sustainability notes. |
| [Governance](./community/governance.md) | `draft` | Decision-making, maintainers, and proposal flow. |
| [Maintainers](./community/maintainers.md) | `draft` | Ownership, responsibility, and escalation contacts. |
| [Expand and collapse](./interactive/expand-collapse.md) | `stable` | Advanced details, troubleshooting, and long examples. |
| [Tabs](./interactive/tabs.md) | `draft` | GitHub-compatible tab-like navigation with anchors. |
| [Terminal blocks](./interactive/terminal-blocks.md) | `stable` | Install, quick start, CLI, deploy, and troubleshooting commands. |
| [Typing headers](./interactive/typing-headers.md) | `experimental` | Animated hero headers and generated typing SVGs. |
| [FAQ](./layout/faq.md) | `stable` | Scope, support, installation, and licensing questions. |
| [Feature grids](./layout/feature-grids.md) | `stable` | Capability tables and compact project summaries. |
| [Hero sections](./layout/hero-sections.md) | `draft` | First-screen README composition. |
| [Roadmap](./layout/roadmap.md) | `draft` | Direction, milestones, and planned work. |
| [Quick Links](./navigation/quick-links.md) | `stable` | Compact top-level links for docs, issues, releases, and examples. |
| [Repository Map](./navigation/repo-map.md) | `stable` | Folder and ownership maps for large repositories. |
| [Role Paths](./navigation/role-paths.md) | `draft` | Different paths for users, contributors, operators, and reviewers. |
| [Start Here](./navigation/start-here.md) | `stable` | First-screen reader routing for busy repositories. |
| [First Run](./onboarding/first-run.md) | `stable` | First successful command path with expected output. |
| [Install Options](./onboarding/install-options.md) | `stable` | Package, source, Docker, and binary installation choices. |
| [Prerequisites](./onboarding/prerequisites.md) | `stable` | Runtime, account, toolchain, and permission requirements. |
| [Troubleshooting Starters](./onboarding/troubleshooting-starters.md) | `draft` | Common failure paths and fixes before users open issues. |
| [Accessibility Notes](./quality/accessibility-notes.md) | `draft` | Accessibility scope, checks, and known gaps. |
| [Observability](./quality/observability.md) | `stable` | Logs, metrics, traces, dashboards, and alerts. |
| [Performance Budget](./quality/performance-budget.md) | `draft` | Performance targets and review thresholds. |
| [Testing Strategy](./quality/testing-strategy.md) | `stable` | Test types, scope, commands, and ownership. |
| [API Reference](./reference/api-reference.md) | `stable` | Endpoint and method summaries that stay readable in GitHub. |
| [CLI Reference](./reference/cli-reference.md) | `stable` | Commands, flags, examples, and output expectations. |
| [Config Reference](./reference/config-reference.md) | `stable` | Environment variables, defaults, and operational impact. |
| [Error Codes](./reference/error-codes.md) | `draft` | Actionable failure tables for support and troubleshooting. |
| [Deprecation Notice](./release/deprecation-notice.md) | `stable` | Clear removal timelines and alternatives. |
| [Release Notes](./release/release-notes.md) | `stable` | Readable release highlights with upgrade risk. |
| [Upgrade Guide](./release/upgrade-guide.md) | `stable` | Migration steps and verification checks. |
| [Version Policy](./release/version-policy.md) | `stable` | Support windows and compatibility commitments. |
| [Dataset status](./status/dataset-status.md) | `draft` | Dataset freshness, quality, and provenance. |
| [Deployment status](./status/deployment-status.md) | `stable` | Production, staging, uptime, and runbook signals. |
| [ML experiments](./status/ml-experiments.md) | `draft` | Experiment tracking, metrics, and model status. |
| [Version lifecycle](./status/version-lifecycle.md) | `stable` | Supported versions, migration, and maintenance windows. |
| [Maintenance Status](./trust/maintenance-status.md) | `stable` | Repository ownership, cadence, and lifecycle expectations. |
| [Provenance](./trust/provenance.md) | `draft` | Source, generation, license, and verification notes. |
| [Security Posture](./trust/security-posture.md) | `stable` | Security boundaries, reporting paths, and reviewed controls. |
| [Support Policy](./trust/support-policy.md) | `stable` | Supported versions, channels, and response boundaries. |

## Machine-Readable Index

Use [`components/index.json`](./index.json) for compatibility data, placeholders, maturity, and generator-ready metadata.

## Copy Checklist

- Replace placeholders.
- Keep links verifiable.
- Keep badge rows short.
- Prefer GitHub-compatible Markdown and HTML.
- Avoid custom JavaScript or external CSS.
