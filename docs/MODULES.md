# Module Pipeline

`src/modules/` is the maintenance pipeline for this repository. It turns the asset library, templates, themes, recipes, and docs into generated indexes, static-site data, QA reports, and release checks. `src/app/` is the local-only browser studio that makes those module outputs interactive without adding a hosted backend.

Use this page when changing tooling, generated files, or the future static showcase site.

## Setup Status

The module pipeline is now a first-class part of the repository setup.

- `site/` is no longer ignored; generated static data and generated review artifacts under `site/data/`, `site/packages/`, `site/reports/`, and `site/svg-contact-sheet.html` are intended to be committed when they change. GIF exports are local-only and default to ignored files under `output/gifs/`.
- `site/index.html`, `site/styles.css`, and `site/app.js` are the frontend-only GitHub Pages showcase shell.
- `npm run build:pages` stages that shell plus every manifest SVG into the ignored `build/pages/` directory, producing a self-contained Pages artifact.
- `assets/manifest.json`, `assets/provenance.json`, and `themes/index.json` are generated repository metadata, not hand-authored source files.
- `npm run generate:all-data` is the canonical regeneration command for the full module data graph.
- `npm run generate:site-data` is intentionally narrower: it regenerates `site/data/assets.json`, `site/data/editor-presets.json`, and `site/data/theme-palettes.json` for the core static showcase/editor path.
- `npm run modules:check` runs the Python CLI aggregate check for generated data freshness and module-level validations.
- `npm run app:dev` starts the local studio at `http://127.0.0.1:8787`.
- `npm run check:app` compiles the local app and runs service self-tests.
- `npm run check:all` remains the release-quality gate and includes module checks, SVG checks, preview freshness, generated-data checks, site data checks, and release readiness.

## Static Gallery Serving

The committed `site/` directory is the source shell, not the complete deployment artifact. It deliberately does not duplicate the 1,058 SVG sources.

For source-tree development, serve the repository root and open `/site/`:

```bash
python -m http.server 8000
```

For the exact self-contained layout deployed to GitHub Pages, build and serve the staged artifact:

```bash
npm run build:pages
python -m http.server 8000 --directory build/pages
```

The staged artifact contains `assets/` beside `index.html`. Gallery previews, editor loads, and downloads therefore use same-origin local files and do not require `raw.githubusercontent.com` or public repository access. Do not serve the raw `site/` directory as the HTTP document root; use one of the two commands above.

## Module Map

| Module | Purpose | Main output or check |
| --- | --- | --- |
| [`generators/`](../src/modules/generators/) | Generate previews, manifests, editor metadata, README SVGs, and editor preset data. | `previews/assets/`, `assets/manifest.json`, `site/data/assets.json` |
| [`editor/`](../src/modules/editor/) | Safely edit SVG colors, text, optional elements, and animation speed. | `site/data/editor-capabilities.json` |
| [`validators/`](../src/modules/validators/) | Check links, template placeholders, theme completeness, raw URLs, and SVG safety. | `npm run check:quality` |
| [`analyzers/`](../src/modules/analyzers/) | Score SVG complexity, motion, size, accessibility, and contrast signals. | `site/data/svg-analysis.json` |
| [`indexers/`](../src/modules/indexers/) | Build searchable asset, template, theme, component, and tag indexes. | `site/data/search-index.json` |
| [`renderers/`](../src/modules/renderers/) | Produce SVG render-smoke metadata, a visual contact sheet, and local SVG-to-GIF exports. | `site/data/svg-render-smoke.json`, `site/svg-contact-sheet.html`, `output/gifs/` |
| [`markdown/`](../src/modules/markdown/) | Check Markdown fences, duplicate anchors, disclosure blocks, table width, and root README shape. | `site/data/markdown-snippets.json` |
| [`themes/`](../src/modules/themes/) | Validate theme examples, color guides, asset maps, and theme registry data. | `themes/index.json`, `site/data/themes.json` |
| [`provenance/`](../src/modules/provenance/) | Convert third-party asset notes into structured provenance metadata. | `assets/provenance.json` |
| [`release/`](../src/modules/release/) | Check release scripts, docs, semantic-release config, generated files, and worktree state. | `npm run check:release-readiness` |
| [`recipes/`](../src/modules/recipes/) | Validate recipe and copy-all bundle links and build site metadata. | `site/data/recipes.json`, `site/data/bundles.json` |
| [`site/`](../src/modules/site/) | Validate the frontend-only static shell, static site data, and generated JSON parity. | `npm run check:site` |
| [`schemas/`](../src/modules/schemas/) | Centralize JSON schema definitions and validate generated data contracts. | `site/data/schema-catalog.json` |
| [`reports/`](../src/modules/reports/) | Build human-readable and machine-readable repository QA reports. | `site/data/quality-report.json`, `site/reports/quality-report.md` |
| [`packagers/`](../src/modules/packagers/) | Build category, theme, starter, and copy-all bundle pack metadata. | `site/data/asset-packs.json`, `site/packages/README.md` |
| [`compatibility/`](../src/modules/compatibility/) | Report GitHub README compatibility risks for Markdown, raw URLs, and SVGs. | `site/data/compatibility-report.json` |
| [`migrations/`](../src/modules/migrations/) | Document and test generated-data schema migration paths. | `site/data/migration-plan.json` |
| [`cli/`](../src/modules/cli/) | One command interface over generation, checks, and summary reports. | `python -m src.modules.cli ...` |
| [`common/`](../src/modules/common/) | Shared repository, Markdown, path, JSON, and link helpers. | Imported by other modules |

## Local Studio

`src/app/` provides a local FastAPI shell around the module pipeline. The browser UI is static HTML, CSS, and JavaScript; the Python layer only serves local generated data, local SVG files, safe SVG edit previews, user-triggered GIF exports, and whitelisted maintenance commands.

```bash
npm run app:dev
```

Open `http://127.0.0.1:8787`.

Use [`src/app/README.md`](../src/app/README.md) for setup, routes, GIF export behavior, command whitelist, and local safety rules.

## Core Commands

Regenerate every generated data artifact:

```bash
npm run generate:all-data
```

Check the full repository:

```bash
npm run check:all
```

Run only the module pipeline:

```bash
npm run modules:check
```

Print a short module inventory:

```bash
npm run modules:report
```

The same workflows are available through the Python CLI:

```bash
python -m src.modules.cli generate
python -m src.modules.cli check
python -m src.modules.cli report
```

## Generated Outputs

These files are generated and should be updated through tooling, not hand-edited:

| Path | Generated by |
| --- | --- |
| `previews/assets/` | `npm run generate:previews` |
| `assets/manifest.json` | `npm run generate:manifest` or `npm run generate:all-data` |
| `assets/provenance.json` | `npm run generate:provenance` or `npm run generate:all-data` |
| `themes/index.json` | `npm run generate:themes` or `npm run generate:all-data` |
| `site/data/assets.json` | `npm run generate:site-data`, `npm run generate:manifest -- --output site/data/assets.json`, or `npm run generate:all-data` |
| `site/data/editor-presets.json` | `npm run generate:editor-data`, `npm run generate:site-data`, or `npm run generate:all-data` |
| `site/data/theme-palettes.json` | `npm run generate:editor-data`, `npm run generate:site-data`, or `npm run generate:all-data` |
| `site/data/editor-capabilities.json` | `npm run generate:editor-capabilities` or `npm run generate:all-data` |
| `site/data/svg-analysis.json` | `npm run generate:analysis` or `npm run generate:all-data` |
| `site/data/search-index.json` | `npm run generate:indexes` or `npm run generate:all-data` |
| `site/data/templates.json` | `npm run generate:indexes` or `npm run generate:all-data` |
| `site/data/components.json` | `npm run generate:indexes` or `npm run generate:all-data` |
| `site/data/tag-index.json` | `npm run generate:indexes` or `npm run generate:all-data` |
| `site/data/markdown-snippets.json` | `npm run generate:markdown-data` or `npm run generate:all-data` |
| `site/data/themes.json` | `npm run generate:themes` or `npm run generate:all-data` |
| `site/data/recipes.json` | `npm run generate:recipes` or `npm run generate:all-data` |
| `site/data/bundles.json` | `npm run generate:recipes` or `npm run generate:all-data` |
| `site/data/svg-render-smoke.json` | `npm run generate:render-smoke` or `npm run generate:all-data` |
| `site/data/compatibility-report.json` | `npm run generate:compatibility` or `npm run generate:all-data` |
| `site/data/asset-packs.json` | `npm run generate:packs` or `npm run generate:all-data` |
| `site/data/quality-report.json` | `npm run generate:reports` or `npm run generate:all-data` |
| `site/data/migration-plan.json` | `npm run generate:migrations` or `npm run generate:all-data` |
| `site/data/schema-catalog.json` | `npm run generate:schemas` or `npm run generate:all-data` |
| `site/svg-contact-sheet.html` | `npm run generate:render-smoke` or `npm run generate:all-data` |
| `site/packages/README.md` | `npm run generate:packs` or `npm run generate:all-data` |
| `site/reports/quality-report.md` | `npm run generate:reports` or `npm run generate:all-data` |

Human-authored source files include `assets/**/*.svg`, `components/**/*.md`, `templates/*.md`, `themes/*/{example.md,colors.md,assets-map.md}`, `docs/*.md`, `src/modules/**/*.py`, and the static showcase shell in `site/index.html`, `site/styles.css`, and `site/app.js`.

## Focused Commands

| Command | Use |
| --- | --- |
| `npm run app:dev` | Start the local-only browser studio. |
| `npm run app:dev:reload` | Start the local studio with uvicorn reload enabled. |
| `npm run check:app` | Compile `src/app/` and run app service self-tests. |
| `npm run generate:previews` | Regenerate visual asset preview pages. |
| `npm run check:previews` | Fail when preview pages are stale. |
| `npm run generate:manifest` | Regenerate the asset manifest. |
| `npm run check:manifest` | Fail when `assets/manifest.json` is stale or invalid. |
| `npm run generate:site-data` | Regenerate core static site asset and editor preset data. |
| `npm run check:site-data` | Check core static site asset and editor preset data. |
| `npm run generate:editor-data` | Regenerate editor preset and palette data. |
| `npm run check:editor-data` | Check editor preset and palette data freshness. |
| `npm run generate:editor-capabilities` | Regenerate safe SVG editor operation metadata. |
| `npm run check:editor` | Check SVG editor operation metadata. |
| `npm run check:generators` | Compile generator scripts and run generator self-tests. |
| `npm run generate:readme-svg` | Generate custom README SVG visuals from presets. |
| `npm run check:svg` | Validate SVG safety and portability. |
| `npm run optimize:svg` | Apply the safe SVG optimization profile. |
| `npm run check:svg:optimize` | Check whether SVGs need safe optimization. |
| `npm run generate:analysis` | Regenerate SVG quality and complexity analysis. |
| `npm run check:analysis` | Check SVG analysis freshness. |
| `npm run generate:indexes` | Regenerate search, template, component, and tag indexes. |
| `npm run check:indexes` | Check index freshness. |
| `npm run generate:markdown-data` | Regenerate reusable Markdown snippet data. |
| `npm run check:markdown` | Check Markdown quality and snippet freshness. |
| `npm run generate:themes` | Regenerate theme registry data. |
| `npm run check:themes` | Check theme docs and generated theme data. |
| `npm run generate:provenance` | Regenerate structured provenance data. |
| `npm run check:provenance` | Check provenance data and third-party source coverage. |
| `npm run generate:recipes` | Regenerate recipe and copy-all bundle data. |
| `npm run check:recipes` | Check recipe and bundle link integrity. |
| `npm run generate:render-smoke` | Regenerate SVG smoke metadata and contact sheet. |
| `npm run check:render-smoke` | Check SVG smoke outputs and blank/invalid render risks. |
| `npm run export:gif -- --asset assets/path/to/asset.svg` | Export a selected SVG to a local GIF under `output/gifs/` by default. |
| `npm run generate:compatibility` | Regenerate GitHub README compatibility report. |
| `npm run check:compatibility` | Check compatibility report freshness and hard errors. |
| `npm run generate:packs` | Regenerate category, theme, starter, and bundle pack metadata. |
| `npm run check:packs` | Check pack metadata and pack index freshness. |
| `npm run generate:reports` | Regenerate quality reports. |
| `npm run check:reports` | Check quality report freshness. |
| `npm run generate:migrations` | Regenerate generated-data migration plan. |
| `npm run check:migrations` | Check migration plan freshness and current schema version. |
| `npm run generate:schemas` | Regenerate schema catalog. |
| `npm run check:schemas` | Check schema definitions and generated data contracts. |
| `npm run check:site` | Check the static site shell/data is frontend-only and internally consistent. |
| `npm run build:pages` | Stage a self-contained Pages artifact with every manifest SVG under `build/pages/`. |
| `npm run check:pages` | Build the Pages artifact in a temporary directory and verify complete local asset coverage. |
| `npm run check:quality` | Run repository quality validators. |
| `npm run check:release-readiness` | Check release configuration, docs, generated outputs, and worktree status. |

## Change Workflows

After changing assets:

```bash
npm run optimize:svg
npm run generate:previews
npm run generate:all-data
npm run check:all
```

After changing templates, components, recipes, themes, or docs:

```bash
npm run generate:all-data
npm run check:all
```

After changing module code:

```bash
npm run generate:all-data
npm run check:modules
npm run check:all
```

After changing schema definitions:

```bash
npm run generate:all-data
npm run check:schemas
npm run check:all
```

## Warning Policy

Some checks emit warnings without failing:

- wide Markdown tables that remain valid but may be hard to browse;
- duplicate subsection anchors in repeated recipe patterns;
- templates that are useful examples but do not use `PROJECT_NAME` or `SERVICE_NAME`;
- dirty worktree state during local development.

Errors fail CI. Warnings should be reviewed before release, but they are allowed when the repository remains valid and generated outputs are current.
