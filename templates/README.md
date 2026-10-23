# Templates

Ready-to-copy README foundations for common project types. Start with the closest match, then layer in assets, themes, and components.

| Template | Maturity | Best for | Contract |
| --- | --- | --- | --- |
| [Backend service](./backend-service.md) | `stable` | APIs and production services | [`contract`](./contracts/backend-service.json) |
| [Browser Extension](./browser-extension.md) | `draft` | Chrome, Firefox, and Edge extensions | [`contract`](./contracts/browser-extension.json) |
| [CLI Tool](./cli-tool.md) | `stable` | Command-line tools, automation helpers, and local developer utilities | [`contract`](./contracts/cli-tool.json) |
| [Course Tutorial](./course-tutorial.md) | `draft` | Learning repositories, workshops, and guided examples | [`contract`](./contracts/course-tutorial.json) |
| [Data Pipeline](./data-pipeline.md) | `stable` | ETL, ELT, batch, streaming, and analytics pipelines | [`contract`](./contracts/data-pipeline.json) |
| [Design System](./design-system.md) | `draft` | Token, component, asset, and documentation systems | [`contract`](./contracts/design-system.json) |
| [Frontend App](./frontend-app.md) | `stable` | Static apps, SPAs, dashboards, and browser-first tools | [`contract`](./contracts/frontend-app.json) |
| [GitHub Action](./github-action.md) | `stable` | Reusable Actions, workflow helpers, and CI automation | [`contract`](./contracts/github-action.json) |
| [Infrastructure IaC](./infrastructure-iac.md) | `stable` | Terraform, Pulumi, Kubernetes, Helm, and platform modules | [`contract`](./contracts/infrastructure-iac.json) |
| [Internal Tool](./internal-tool.md) | `draft` | Admin panels, operations tools, and private workflow apps | [`contract`](./contracts/internal-tool.json) |
| [Minimal](./minimal.md) | `stable` | Small tools, utilities, and focused repos | [`contract`](./contracts/minimal.json) |
| [ML project](./ml-project.md) | `draft` | Model training, evaluation, and inference repos | [`contract`](./contracts/ml-project.json) |
| [Mobile App](./mobile-app.md) | `draft` | iOS, Android, React Native, Flutter, and cross-platform apps | [`contract`](./contracts/mobile-app.json) |
| [Monorepo](./monorepo.md) | `draft` | Multi-package repositories with shared tooling and ownership boundaries | [`contract`](./contracts/monorepo.json) |
| [Open-source library](./open-source-lib.md) | `stable` | Published packages and reusable libraries | [`contract`](./contracts/open-source-lib.json) |
| [Plugin Extension](./plugin-extension.md) | `draft` | Editor plugins, app extensions, and integration packages | [`contract`](./contracts/plugin-extension.json) |
| [Portfolio Profile](./portfolio-profile.md) | `draft` | Personal GitHub profiles, portfolios, and professional showcases | [`contract`](./contracts/portfolio-profile.json) |
| [Research project](./research-project.md) | `draft` | Papers, experiments, and reproducibility repos | [`contract`](./contracts/research-project.json) |
| [SaaS Product](./saas-product.md) | `draft` | Product repositories with docs, operations, support, and launch context | [`contract`](./contracts/saas-product.json) |
| [SDK Reference](./sdk-reference.md) | `stable` | SDKs with install, auth, API examples, and compatibility promises | [`contract`](./contracts/sdk-reference.json) |
| [Spec RFC](./spec-rfc.md) | `draft` | Specifications, proposals, standards, and design docs | [`contract`](./contracts/spec-rfc.json) |

## Maturity

| Marker | Meaning |
| --- | --- |
| `stable` | Ready for broad reuse after placeholder replacement. |
| `draft` | Useful and complete, but likely needs closer project-specific editing. |
| `experimental` | Reserved for templates with high-expression or advanced patterns. |

For the full maturity policy, see [Design maturity](../docs/MATURITY.md).

## Use With

- [Themes](../themes/) for visual direction.
- [Components](../components/) for focused sections.
- [Asset previews](../previews/assets/README.md) for copyable SVG snippets.
- [`templates/index.json`](./index.json) for generator-ready metadata.

## Customization Checklist

- Replace placeholder project names and commands.
- Remove sections that do not apply.
- Update badges and links.
- Add real examples.
- Confirm all copied asset links render correctly.
