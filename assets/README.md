# Assets

The `assets/` directory contains the SVG library used by the templates, themes, components, and generated preview pages.

Use the generated preview catalog first when browsing assets:

- [Asset preview index](../previews/assets/README.md)
- [Banners](../previews/assets/banners.md)
- [Buttons](../previews/assets/buttons.md)
- [Dividers](../previews/assets/dividers.md)
- [Headers](../previews/assets/headers.md)
- [Icons](../previews/assets/icons.md)
- [Loadings](../previews/assets/loadings.md)
- [File headers](../previews/assets/file_headers.md)

## Categories

| Category | Purpose | Preview |
| --- | --- | --- |
| `banners/` | Wide visual strips for hero areas, section breaks, and visual identity. | [Preview](../previews/assets/banners.md) |
| `buttons/` | SVG call-to-action, social, profile, and status buttons for README links. | [Preview](../previews/assets/buttons.md) |
| `dividers/` | Static and animated separators between README sections. | [Preview](../previews/assets/dividers.md) |
| `file_headers/` | Header graphics for repository files such as `README.md`, `SECURITY.md`, and `CHANGELOG.md`. | [Preview](../previews/assets/file_headers.md) |
| `headers/` | Title and section header graphics. | [Preview](../previews/assets/headers.md) |
| `icons/` | Small symbols for UI, status, data, development, effects, and navigation. | [Preview](../previews/assets/icons.md) |
| `loadings/` | Animated loading indicators and motion accents. | [Preview](../previews/assets/loadings.md) |
| `personal/` | Profile README, portfolio, and project-story visuals. | [Preview](../previews/assets/personal.md) |
| `progress_bars/` | Progress, lifecycle, and completion indicators. | [Preview](../previews/assets/progress_bars.md) |
| `visuals/` | Larger conceptual illustrations for systems, AI, infrastructure, and collaboration. | [Preview](../previews/assets/visuals.md) |

## Usage

Use raw GitHub URLs when embedding assets from this repository:

```markdown
![Header](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_minimal_lux.svg)
```

Use relative paths when copying assets into another repository:

```markdown
![Header](./assets/headers/static/header_minimal_lux.svg)
```

## Tags

Generated preview pages include asset tags for compact scanning. Tags are inferred from:

- Top-level category, such as `icon`, `loading`, `header`, `visual`, or `progress`.
- Subcategory, such as `minimal`, `animated`, `data`, `devops`, `navigation`, or `status`.
- SVG behavior, such as `animated`, `motion`, or `static`.
- Filename keywords, such as `ai`, `security`, `terminal`, `pipeline`, `docs`, `testing`, or `profile`.

Use descriptive filenames and the right asset folder when adding assets; the preview generator will assign the tags during `npm run generate:previews`.

## Adding Assets

Before adding or changing SVGs, read:

- [Contributing guide](../CONTRIBUTING.md)
- [Visual style guide](../docs/VISUAL_STYLE.md)
- [Asset deprecation policy](../docs/ASSET_DEPRECATION.md)

After asset changes, regenerate previews:

```bash
npm run optimize:svg
npm run generate:previews
npm run check:all
```

Generated preview files under `previews/assets/` are committed output and should not be edited by hand.

See [SVG optimization](../docs/SVG_OPTIMIZATION.md) for the safe optimizer profile and why aggressive SVG rewrites are avoided by default.
