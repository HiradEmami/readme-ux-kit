# Navigation

Use this page as the repository map for `readme-ux-kit`.

## Start Here

| Need | Go to |
| --- | --- |
| Browse SVG assets visually | [`previews/assets/README.md`](./previews/assets/README.md) |
| Pick a README foundation | [`templates/README.md`](./templates/README.md) |
| Pick a visual direction | [`themes/README.md`](./themes/README.md) |
| Copy focused README sections | [`components/README.md`](./components/README.md) |
| Paste a complete README starter | [`docs/BUNDLES.md`](./docs/BUNDLES.md) |
| Assemble a complete README quickly | [`docs/RECIPES.md`](./docs/RECIPES.md) |
| See real-world usage examples | [`docs/SHOWCASE.md`](./docs/SHOWCASE.md) |
| Add or review assets | [`CONTRIBUTING.md`](./CONTRIBUTING.md) |

## Asset Browsing

| Category | Preview | Source |
| --- | --- | --- |
| Banners | [`previews/assets/banners.md`](./previews/assets/banners.md) | [`assets/banners/`](./assets/banners/) |
| Dividers | [`previews/assets/dividers.md`](./previews/assets/dividers.md) | [`assets/dividers/`](./assets/dividers/) |
| File headers | [`previews/assets/file_headers.md`](./previews/assets/file_headers.md) | [`assets/file_headers/`](./assets/file_headers/) |
| Headers | [`previews/assets/headers.md`](./previews/assets/headers.md) | [`assets/headers/`](./assets/headers/) |
| Icons | [`previews/assets/icons.md`](./previews/assets/icons.md) | [`assets/icons/`](./assets/icons/) |
| Loadings | [`previews/assets/loadings.md`](./previews/assets/loadings.md) | [`assets/loadings/`](./assets/loadings/) |
| Personal | [`previews/assets/personal.md`](./previews/assets/personal.md) | [`assets/personal/`](./assets/personal/) |
| Progress bars | [`previews/assets/progress_bars.md`](./previews/assets/progress_bars.md) | [`assets/progress_bars/`](./assets/progress_bars/) |
| Visuals | [`previews/assets/visuals.md`](./previews/assets/visuals.md) | [`assets/visuals/`](./assets/visuals/) |

## Templates

| Template | Use |
| --- | --- |
| [`templates/minimal.md`](./templates/minimal.md) | Small tools, focused repos, and simple project pages. |
| [`templates/backend-service.md`](./templates/backend-service.md) | APIs, services, workers, and production systems. |
| [`templates/ml-project.md`](./templates/ml-project.md) | Model training, evaluation, data, and inference projects. |
| [`templates/open-source-lib.md`](./templates/open-source-lib.md) | Libraries, packages, SDKs, and reusable modules. |
| [`templates/research-project.md`](./templates/research-project.md) | Papers, experiments, and reproducibility repositories. |

## Themes

| Theme | Use |
| --- | --- |
| [`themes/minimal/example.md`](./themes/minimal/example.md) | Quiet, polished, low-noise READMEs. |
| [`themes/terminal/example.md`](./themes/terminal/example.md) | CLI-first tools and automation workflows. |
| [`themes/ai-neural/example.md`](./themes/ai-neural/example.md) | AI, ML, data, and research projects. |
| [`themes/cyberpunk/example.md`](./themes/cyberpunk/example.md) | Security, DevOps, infrastructure, and high-energy technical repos. |
| [`themes/cyberpunk/colors.md`](./themes/cyberpunk/colors.md) | Cyberpunk color system. |
| [`themes/cyberpunk/assets-map.md`](./themes/cyberpunk/assets-map.md) | Cyberpunk asset recommendations. |

## Components

| Component group | Use |
| --- | --- |
| [`components/badges/`](./components/badges/) | Build, release, package, system, and signal badge rows. |
| [`components/interactive/`](./components/interactive/) | GitHub-compatible collapsible sections, tabs, terminal blocks, and typing headers. |
| [`components/layout/`](./components/layout/) | Hero sections, feature grids, FAQs, and roadmaps. |
| [`components/status/`](./components/status/) | Deployment, dataset, experiment, and version lifecycle sections. |

## Maintainer Docs

| Doc | Purpose |
| --- | --- |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | Contribution workflow, asset rules, SVG quality checks, and PR expectations. |
| [`docs/CONTRIBUTOR_QUICKSTART.md`](./docs/CONTRIBUTOR_QUICKSTART.md) | Shortest workflows for adding one asset, component, template, or generator change. |
| [`SECURITY.md`](./SECURITY.md) | Security reporting and SVG safety scope. |
| [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) | Community behavior expectations. |
| [`docs/BUNDLES.md`](./docs/BUNDLES.md) | Copy-all README starter bundles. |
| [`docs/CHANGELOG.md`](./docs/CHANGELOG.md) | Changelog discipline, commit scopes, and release-note rules. |
| [`docs/LIMITATIONS.md`](./docs/LIMITATIONS.md) | Known GitHub Markdown, SVG, badge, raw URL, and preview limitations. |
| [`docs/MATURITY.md`](./docs/MATURITY.md) | Stability markers for components and templates. |
| [`docs/RECIPES.md`](./docs/RECIPES.md) | Complete README assembly recipes. |
| [`docs/README_SVG_GENERATORS.md`](./docs/README_SVG_GENERATORS.md) | Typing and multi-preset SVG generator examples. |
| [`docs/SHOWCASE.md`](./docs/SHOWCASE.md) | Community usage examples and submission rules. |
| [`docs/SVG_OPTIMIZATION.md`](./docs/SVG_OPTIMIZATION.md) | Safe SVG optimization profile and workflow. |
| [`docs/VISUAL_STYLE.md`](./docs/VISUAL_STYLE.md) | Visual style, color, animation, layout, and accessibility guidance. |
| [`docs/TYPING_SVG_EXAMPLES.md`](./docs/TYPING_SVG_EXAMPLES.md) | Examples for the typing SVG generator. |
| [`docs/ASSET_DEPRECATION.md`](./docs/ASSET_DEPRECATION.md) | Policy for renaming, replacing, deprecating, and removing assets. |
| [`docs/THIRD_PARTY.md`](./docs/THIRD_PARTY.md) | Third-party asset provenance and license notes. |

## Tooling

| Command | Purpose |
| --- | --- |
| `npm run generate:previews` | Regenerate committed preview pages under `previews/assets/`. |
| `npm run check:previews` | Verify generated previews are current. |
| `npm run check:generators` | Compile Python generator scripts. |
| `npm run check:svg` | Validate SVG safety and portability. |
| `npm run optimize:svg` | Apply safe SVG whitespace/comment optimization. |
| `npm run check:svg:optimize` | Report SVG files that would change under the safe optimizer. |
| `npm run check:all` | Run all repository quality checks. |

## Release And Automation

| File | Purpose |
| --- | --- |
| [`.github/workflows/quality.yml`](./.github/workflows/quality.yml) | CI quality checks for PRs and `master`. |
| [`.github/workflows/semantic_release.yml`](./.github/workflows/semantic_release.yml) | Manual semantic-release workflow with pre-release quality checks. |
| [`.releaserc.json`](./.releaserc.json) | Semantic-release configuration. |
| [`CHANGELOG.md`](./CHANGELOG.md) | Generated release history. |
| [`docs/RELEASE.md`](./docs/RELEASE.md) | Maintainer release policy and workflow steps. |
| [`package.json`](./package.json) | Maintenance scripts and release dependencies. |
