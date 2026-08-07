# Contributing

Thanks for improving `readme-ux-kit`. This repository is a GitHub-native README design kit, so contributions should be easy to browse, easy to copy, and safe to render in GitHub Markdown.

## What to Contribute

Good contributions usually fall into one of these groups:

- new SVG assets under `assets/`
- improved Markdown components under `components/`
- stronger starter templates under `templates/`
- theme examples under `themes/`
- generator improvements under `src/modules/generators/`
- community showcase entries under `docs/SHOWCASE.md`
- documentation and preview fixes

Keep pull requests focused. A new asset set, a template improvement, and a generator refactor should usually be separate PRs.

For the shortest command-by-command workflow, see `docs/CONTRIBUTOR_QUICKSTART.md`.

## Add an Asset

1. Choose the right top-level category under `assets/`.
2. Use an existing subcategory if one matches the asset.
3. Create a new subcategory only when it improves discovery for future assets.
4. Add the SVG file.
5. Regenerate previews.
6. Run the preview freshness check.
7. Include a short PR note describing the asset purpose and where it should be used.

Example:

```text
assets/
`-- banners/
    `-- energy/
        `-- banner_signal_beam.svg
```

After adding the file:

```bash
python src/modules/generators/generate_asset_previews.py
python src/modules/generators/generate_asset_previews.py --check
```

## Asset Categories

Use the existing category system unless there is a clear reason to expand it.

| Category | Use |
| --- | --- |
| `banners/` | Wide visual strips for hero areas and section breaks. |
| `dividers/` | Horizontal separators between README sections. |
| `file_headers/` | Graphics for repository files such as `SECURITY.md` and `CONTRIBUTING.md`. |
| `headers/` | Title and section header graphics. |
| `icons/` | Small symbols for status, UI, development, navigation, and concepts. |
| `loadings/` | Loading indicators and motion accents. |
| `personal/` | Profile README, portfolio, and author/project-story visuals. |
| `progress_bars/` | Progress, lifecycle, and completion indicators. |
| `visuals/` | Larger conceptual illustrations. |

## Naming Rules

Use lowercase snake case for asset filenames:

```text
category_subject_variant.svg
```

Good examples:

```text
banner_signal_beam.svg
divider_neural_pulse.svg
icon_pipeline_status.svg
header_terminal_typing.svg
loading_orbiting_dots.svg
```

Rules:

- Use only lowercase letters, numbers, and underscores.
- Use a category prefix when the folder contains a specific asset type: `banner_`, `divider_`, `header_`, `icon_`, `loading_`, or `progress_bar_`.
- Keep names descriptive enough to understand without opening the file.
- Avoid vague names such as `new.svg`, `final.svg`, `cool_icon.svg`, or `asset_01.svg`.
- Avoid typos and inconsistent plurals.
- Do not rename existing assets in the same PR as unrelated changes, because raw GitHub links may already be in use.

## SVG Quality Rules

SVG assets should be GitHub-friendly, lightweight, and safe to embed.

For broader design guidance, see `docs/VISUAL_STYLE.md`. For renaming or replacing assets, see `docs/ASSET_DEPRECATION.md`.

Required:

- Include a valid root `<svg>` element.
- Include a `viewBox`.
- Prefer scalable dimensions over hard-coded layouts that only work at one size.
- Keep the file self-contained; no external fonts, images, scripts, or remote resources.
- Use semantic grouping and readable IDs when practical.
- Keep animation inside SVG/CSS only.
- Make sure the asset renders on both GitHub light and dark themes when possible.
- Use transparent backgrounds unless the design intentionally needs a fixed background.
- Keep text minimal inside SVG assets; README users cannot easily localize or edit embedded text.

Avoid:

- `<script>` tags.
- external CSS or external image references.
- editor metadata blocks that add large noisy output.
- raster images embedded as base64 unless there is a strong reason.
- huge path data from unoptimized exports when a smaller equivalent is possible.
- flashing or very aggressive animation.

Recommended checks before submitting:

- Open the SVG locally or in a browser.
- View it at small and large sizes.
- Confirm it does not clip at the edges.
- Confirm animation loops cleanly if animated.
- Confirm the visual meaning is obvious from the filename and category.
- Run `npm run optimize:svg` to apply the safe non-destructive optimization profile.

## Markdown Component Rules

Markdown snippets should work in GitHub README rendering.

Use:

- standard Markdown tables
- fenced code blocks
- raw GitHub image URLs for kit assets
- GitHub-compatible HTML such as `<p>`, `<img>`, `<a>`, `<details>`, and `<summary>`

Avoid:

- custom JavaScript
- custom external CSS
- layout that depends on unsupported GitHub styling
- very wide tables that become unreadable on smaller screens
- claims that cannot be copied into another repository safely

Every component should explain:

- what it is for
- when to use it
- a copyable example
- any customization notes

## Design Maturity Markers

Components and templates should include a visible maturity marker near the top of the file:

```markdown
> Maturity: `stable`
```

Use:

- `stable` for snippets that are ready for broad reuse after placeholder replacement.
- `draft` for useful snippets that still need closer project-specific editing.
- `experimental` for high-expression, motion-heavy, or advanced patterns that need extra visual and accessibility review.

Update `components/README.md`, `templates/README.md`, and `docs/MATURITY.md` when adding or changing component/template maturity.

## Regenerate Previews

Generated asset previews live under:

```text
previews/assets/
```

These generated files are committed output. They are intentionally kept in the repository because users browse them directly on GitHub, and because the preview pages contain copyable Markdown and HTML snippets.

Regenerate them after adding, moving, renaming, or deleting SVG assets:

```bash
python src/modules/generators/generate_asset_previews.py
```

Check that committed previews are current:

```bash
python src/modules/generators/generate_asset_previews.py --check
```

The `--check` mode is intended for CI. It generates previews in a temporary directory, compares them with `previews/assets/`, and exits with code `1` when files are missing, changed, or extra.

Do not hand-edit generated files under `previews/assets/`. If preview content needs to change, update `src/modules/generators/generate_asset_previews.py`, regenerate the previews, and commit both the generator change and generated output.

For generated typing headers, see `docs/TYPING_SVG_EXAMPLES.md`.

## Review Checks

Before requesting review, run the checks that match your change.

For asset changes:

```bash
python src/modules/generators/generate_asset_previews.py
python src/modules/generators/generate_asset_previews.py --check
```

For generator changes:

```bash
python -m py_compile src/modules/generators/generate_asset_previews.py
python -m py_compile src/modules/generators/generate_typing_svg.py
python src/modules/generators/generate_asset_previews.py --check
```

For documentation-only changes:

```bash
git diff --check
```

PR checklist:

- [ ] The change is focused and belongs in this repository.
- [ ] New assets follow the naming rules.
- [ ] SVGs include a `viewBox` and do not depend on external resources.
- [ ] Generated previews were regenerated when assets changed.
- [ ] `generate_asset_previews.py --check` passes.
- [ ] Markdown examples render in GitHub-compatible Markdown.
- [ ] New or changed links point to real files or intended external pages.
- [ ] Third-party assets are documented in `docs/THIRD_PARTY.md` when needed.

## Third-Party Assets

If an asset comes from another source, document it in `docs/THIRD_PARTY.md`.

Include:

- source URL
- original license
- local file paths
- whether the asset is original or a modified derivative
- what was modified, if anything
- whether attribution is required

Do not add assets unless the license allows redistribution in this repository.

## Showcase Entries

Community showcase entries live in `docs/SHOWCASE.md`.

Only add public repositories that visibly use this kit and provide a useful example for future users. Include what was used, what pattern the README demonstrates, and why it is a good reference. Do not add private repositories, unrelated projects, or promotional entries that do not teach a reusable README pattern.

## Commit Messages

Use clear, conventional commit-style messages when possible:

```text
feat(assets): add energy banner set
docs(templates): improve backend service template
fix(previews): regenerate stale asset previews
chore(release): update semantic-release config
```

Prefer scopes that keep generated changelogs readable: `assets`, `templates`, `themes`, `components`, `previews`, `generators`, `docs`, `ci`, and `release`.

See `docs/CHANGELOG.md` for changelog discipline and release-note expectations.

## Maintainer Review Standard

A contribution is ready when it improves reuse, discoverability, or quality without making the kit harder to browse or maintain. Prefer fewer, sharper assets and examples over large batches that are inconsistent or difficult to preview.
