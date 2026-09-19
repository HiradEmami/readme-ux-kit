# readme-ux-kit

A GitHub-native README design kit with copyable SVG assets, templates, themes, components, bundles, generators, and quality tooling.

[![Quality](https://github.com/HiradEmami/readme-ux-kit/actions/workflows/quality.yml/badge.svg?branch=master)](https://github.com/HiradEmami/readme-ux-kit/actions/workflows/quality.yml)
[![Preview freshness](https://img.shields.io/badge/previews-checked-16a34a?style=flat-square)](https://github.com/HiradEmami/readme-ux-kit/actions/workflows/quality.yml)
[![SVG validation](https://img.shields.io/badge/svg-validated-2563eb?style=flat-square)](https://github.com/HiradEmami/readme-ux-kit/actions/workflows/quality.yml)
[![Release](https://img.shields.io/github/v/release/HiradEmami/readme-ux-kit?style=flat-square&label=release&color=7c3aed)](https://github.com/HiradEmami/readme-ux-kit/releases)
[![License](https://img.shields.io/github/license/HiradEmami/readme-ux-kit?style=flat-square&color=475569)](./LICENSE)

Use this kit when you want a polished README without building a custom docs site.

[![Readme UX Kit banner](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/banners/minimal/banner_premium_minimal_dot.svg)](https://github.com/HiradEmami/readme-ux-kit)

## Start Here

| Step | Action | Start with |
| --- | --- | --- |
| 1 | Browse assets | [`previews/assets/`](./previews/assets/README.md) |
| 2 | Pick a template | [`templates/`](./templates/README.md) |
| 3 | Pick a theme | [`themes/`](./themes/README.md) |
| 4 | Copy components | [`components/`](./components/README.md) |
| 5 | Paste a full starter | [`docs/BUNDLES.md`](./docs/BUNDLES.md) |

For the full repository map, see [`NAVIGATION.md`](./NAVIGATION.md).

## What You Get

| Area | Use |
| --- | --- |
| [`assets/`](./assets/README.md) | SVG banners, badges, buttons, callouts, cards, charts, diagrams, headers, icons, loaders, mockups, panels, progress bars, and visuals. |
| [`previews/assets/`](./previews/assets/README.md) | Generated visual previews with source links, raw links, tags, and copyable snippets. |
| [`templates/`](./templates/README.md) | README foundations for libraries, services, ML projects, research projects, and minimal repos. |
| [`components/`](./components/README.md) | Badges, layouts, status sections, terminal blocks, tabs, and collapsible patterns. |
| [`themes/`](./themes/README.md) | Visual directions with recommended assets and examples. |
| [`docs/BUNDLES.md`](./docs/BUNDLES.md) | Complete copy-all README starters. |
| [`src/modules/`](./docs/MODULES.md) | Generators, validators, analyzers, indexes, editor metadata, reports, packs, compatibility checks, and release gates. |
| [`src/app/`](./src/app/README.md) | Local-only browser studio for asset search, snippet copy, SVG edits, GIF exports, reports, and whitelisted checks. |

Specialist asset families: [`badges/`](./assets/badges/), [`callouts/`](./assets/callouts/), [`cards/`](./assets/cards/), [`charts/`](./assets/charts/), [`diagrams/`](./assets/diagrams/), [`mockups/`](./assets/mockups/), [`terminal_panels/`](./assets/terminal_panels/), and [`workflow_panels/`](./assets/workflow_panels/).

## Quick Copy

Use raw GitHub URLs when embedding assets from this repository:

```markdown
![Loading animation](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/loadings/loading_bouncing_dots.svg)
```

Use relative paths when copying assets into your own repository:

```markdown
![Loading animation](./assets/loadings/loading_bouncing_dots.svg)
```

SVG is the primary format. GIF export is local-only through `npm run app:dev` or `npm run export:gif -- --asset assets/path/to/asset.svg`; see [`docs/GIF_EXPORTS.md`](./docs/GIF_EXPORTS.md).

## Common Commands

```bash
npm run generate:all-data
npm run modules:report
npm run generate:previews
npm run check:all
npm run app:dev
```

Preview the same self-contained static gallery that GitHub Pages deploys:

```bash
npm run build:pages
python -m http.server 8000 --directory build/pages
```

Generate custom README visuals:

```bash
npm run generate:readme-svg -- --preset wave-banner --title "Project Name" --output banner.svg
python src/modules/generators/generate_typing_svg.py --text "Build faster" --output typing.svg
```

## Maintainer Docs

- [Contributor quickstart](./docs/CONTRIBUTOR_QUICKSTART.md)
- [Visual style guide](./docs/VISUAL_STYLE.md)
- [README SVG generators](./docs/README_SVG_GENERATORS.md)
- [SVG to GIF exports](./docs/GIF_EXPORTS.md)
- [Module pipeline](./docs/MODULES.md)
- [Known limitations](./docs/LIMITATIONS.md)
- [Design maturity markers](./docs/MATURITY.md)
- [Changelog discipline](./docs/CHANGELOG.md)
- [Release process](./docs/RELEASE.md)
- [Third-party asset provenance](./docs/THIRD_PARTY.md)

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for asset naming rules, SVG quality guidelines, preview regeneration, and review checks.

## License

This project is licensed under the MIT License. Some file-header SVGs are documented separately in [third-party asset provenance](./docs/THIRD_PARTY.md).
