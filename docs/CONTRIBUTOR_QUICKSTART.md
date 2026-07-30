# Contributor Quickstart

Use this when you want the shortest safe path for a focused contribution.

## Before You Start

Run the full check once so you know your baseline:

```bash
npm run check:all
```

Expected result:

```text
generate_asset_previews.py self-tests passed.
Validated ... SVG assets.
Asset previews are current.
```

Keep the pull request focused. Asset additions, component rewrites, template changes, and generator changes should usually be separate PRs.

## Add One SVG Asset

1. Pick the right folder under `assets/`.
2. Use lowercase snake case and the category prefix when appropriate.
3. Add the SVG.
4. Optimize safely.
5. Regenerate previews.
6. Run checks.

Example:

```text
assets/progress_bars/progress_bar_release_readiness.svg
```

Commands:

```bash
npm run optimize:svg
npm run generate:previews
npm run check:all
```

Expected result:

```text
Generated previews for 9 asset categories in .../previews/assets
Validated ... SVG assets.
Asset previews are current.
```

For faster local iteration on one category:

```bash
python src/modules/generators/generate_asset_previews.py --category progress_bars
python src/modules/generators/generate_asset_previews.py --check --category progress_bars
```

Before opening the PR:

- Confirm the SVG has a valid `viewBox`.
- Confirm there are no external resources, scripts, or embedded raster blobs.
- Confirm the asset renders in GitHub light and dark mode when possible.
- Confirm the generated preview page includes the new asset.
- Update `docs/THIRD_PARTY.md` if the asset came from another source.

## Add One Component

1. Pick the matching component group under `components/`.
2. Add or edit one Markdown file.
3. Include a maturity marker near the top.
4. Include a copyable fenced Markdown example.
5. Update `components/README.md` if a new component file is added.
6. Run checks.

Example maturity marker:

```markdown
> Maturity: `stable`
```

Commands:

```bash
npm run check:all
git diff --check
```

Expected result:

```text
Asset previews are current.
```

Use maturity carefully:

| Marker | Use when |
| --- | --- |
| `stable` | The snippet is broadly reusable after placeholder replacement. |
| `draft` | The snippet works but needs closer project-specific editing. |
| `experimental` | The snippet is high-expression, motion-heavy, or visually risky. |

Before opening the PR:

- Replace fake final claims with placeholders such as `OWNER`, `REPO`, or `PROJECT_NAME`.
- Keep tables readable on GitHub.
- Avoid custom JavaScript and external CSS.
- Link assets with raw GitHub URLs when examples are meant to be copyable.

## Add One Template

1. Add or edit a file under `templates/`.
2. Keep the template complete enough to be useful, but easy to delete from.
3. Include a maturity marker near the top.
4. Update `templates/README.md`.
5. If the template changes a bundle or recipe, update `docs/BUNDLES.md` or `docs/RECIPES.md`.
6. Run checks.

Template starter:

```markdown
# Project Name

> Maturity: `draft`

> One clear sentence about the project, audience, and outcome.

## Quick Start

```bash
command goes here
```
```

Commands:

```bash
npm run check:all
git diff --check
```

Before opening the PR:

- Keep sections broadly useful.
- Use placeholders instead of making unverifiable claims.
- Include install or quick start near the top.
- Include security, license, or maintenance sections when relevant.

## Change A Generator

Generator changes affect committed output, so update both the script and generated files.

Commands:

```bash
python -m py_compile src/modules/generators/generate_asset_previews.py
python src/modules/generators/generate_asset_previews.py --self-test
npm run generate:previews
npm run check:all
```

Expected result:

```text
generate_asset_previews.py self-tests passed.
Asset previews are current.
```

Before opening the PR:

- Explain whether generated output changed.
- Keep generated files under `previews/assets/` committed.
- Do not hand-edit generated preview files.

## PR Checklist

- [ ] The PR has one clear purpose.
- [ ] New assets follow naming and SVG safety rules.
- [ ] Components/templates include maturity markers when relevant.
- [ ] Generated previews were regenerated when assets or generator behavior changed.
- [ ] `npm run check:all` passes.
- [ ] Third-party sources are documented in `docs/THIRD_PARTY.md` when relevant.
