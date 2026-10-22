# Third-Party Notices & Dependency Attribution

This document lists all third-party open-source packages, runtime dependencies, and derived visual assets used or referenced by `readme-ux-kit`.

## 1. Repository License

`readme-ux-kit` is licensed under the **MIT License** (`SPDX-License-Identifier: MIT`). See [`LICENSE`](LICENSE) for the full text.

## 2. Browser Showcase (`site/`) Runtime Dependencies

The static browser showcase (`site/index.html`, `site/styles.css`, `site/app.js`) ships **zero third-party JavaScript or CSS runtime dependencies**.

## 3. Local Studio (`src/pyproject.toml`) Python Dependencies

Used only when running the local studio (`npm run app:dev`) or local GIF export (`npm run export:gif`):

| Package | Version Constraint | SPDX License | Purpose |
| --- | --- | --- | --- |
| `fastapi` | `>=0.116.0` | `MIT` | Local-only loopback HTTP API server (`src/app/api.py`). |
| `uvicorn` | `>=0.35.0` | `BSD-3-Clause` | ASGI server for Local Studio (`src/app/__main__.py`). |
| `pillow` | `>=11.0.0` | `MIT-CMU` | Frame quantization and GIF assembly (`src/modules/renderers/svg_to_gif.py`). |
| `playwright` | `>=1.46.0` | `Apache-2.0` | Headless Chromium frame capture for local SVG-to-GIF export. |
| `tzdata` | `>=2026.3` | `Apache-2.0` | IANA time zone database for Python standard library. |

## 4. Node.js Release Tooling (`package.json` `devDependencies`)

Used exclusively in CI release workflows (`semantic-release`):

| Package | Version | SPDX License | Purpose |
| --- | --- | --- | --- |
| `semantic-release` | `^25.0.3` | `MIT` | Automated semantic versioning and release publishing. |
| `@semantic-release/changelog` | `^6.0.3` | `MIT` | Updates `CHANGELOG.md` during automated releases. |
| `@semantic-release/commit-analyzer` | `^13.0.1` | `MIT` | Parses Conventional Commit messages. |
| `@semantic-release/git` | `^10.0.1` | `MIT` | Commits release artifacts in CI. |
| `@semantic-release/github` | `^12.0.6` | `MIT` | Publishes GitHub Releases. |
| `@semantic-release/release-notes-generator` | `^14.1.0` | `MIT` | Generates structured release notes. |

## 5. Third-Party Derived SVG Assets

Nine file-header SVGs under `assets/file_headers/` were adapted from [`OstinUA/Promt-AI-Helper`](https://github.com/OstinUA/Promt-AI-Helper) released under **The Unlicense** (public domain dedication). Full per-file provenance, SHA-256 checksums, and modification notes are documented in [`docs/THIRD_PARTY.md`](docs/THIRD_PARTY.md), [`ASSET_PROVENANCE.md`](ASSET_PROVENANCE.md), and [`assets/provenance.json`](assets/provenance.json).
