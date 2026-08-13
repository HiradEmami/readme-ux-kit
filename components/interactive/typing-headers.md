# Typing Headers

> Maturity: `experimental`

Animated typing headers give a README a strong first impression without requiring JavaScript. This kit includes ready-made animated SVG headers and a generator for creating custom text.

Use typing headers for short positioning lines, status phrases, product names, or concise project promises. Keep them readable and restrained.

## Ready-Made Header

```markdown
<p align="center">
  <img alt="Animated typing header" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/animated/header_typing_dots.svg">
</p>
```

## Premium Hero Header

```markdown
<p align="center">
  <img alt="Project header" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/animated/header_scanning_status.svg">
</p>

<p align="center">
  <strong>Fast builds. Clear docs. Reliable releases.</strong>
</p>
```

## Generate A Custom Typing SVG

Run the generator from the repository root:

```bash
python src/modules/generators/generate_typing_svg.py \
  --text "Ship polished READMEs faster" \
  --text-color "#38bdf8" \
  --font-size 56 \
  --font-family "'Courier New', Consolas, monospace" \
  --width 1000 \
  --duration 3.8 \
  --steps 34 \
  --output assets/headers/animated/custom_readme_header.svg
```

Embed the generated asset:

```markdown
<p align="center">
  <img alt="Ship polished READMEs faster" src="./assets/headers/animated/custom_readme_header.svg">
</p>
```

## Compact Typing Line

```bash
python src/modules/generators/generate_typing_svg.py \
  --text "npm install. Import. Build." \
  --text-color "#16a34a" \
  --font-size 42 \
  --width 760 \
  --duration 3 \
  --steps 28 \
  --output assets/headers/animated/install_typing.svg
```

```markdown
<img alt="npm install. Import. Build." src="./assets/headers/animated/install_typing.svg">
```

## Dark Interface Header

```markdown
<p align="center">
  <img alt="System status header" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_status_dashboard.svg">
</p>

<p align="center">
  <img alt="Scanning status animation" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/animated/header_horizontal_scanning.svg">
</p>
```

## Header With Badges

```markdown
<p align="center">
  <img alt="Project status" src="./assets/headers/animated/custom_readme_header.svg">
</p>

<p align="center">
  <a href="https://github.com/OWNER/REPO/actions">
    <img alt="Build" src="https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=for-the-badge&label=build&color=16a34a">
  </a>
  <a href="https://github.com/OWNER/REPO/releases">
    <img alt="Release" src="https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=release&color=2563eb">
  </a>
  <a href="../../LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&color=475569">
  </a>
</p>
```

## Text Recipes

```text
Open-source library:   "Install once. Ship everywhere."
Backend service:       "Typed APIs. Observable jobs. Clean deploys."
AI project:            "Evaluate. Improve. Deploy with confidence."
Portfolio:             "Design-minded engineering for real products."
Research project:      "Reproducible experiments. Transparent results."
Developer tool:        "One command from idea to production."
```

## Sizing Guidance

| Use case | Width | Font size | Duration |
| --- | ---: | ---: | ---: |
| Full hero | `900` to `1100` | `52` to `72` | `3.5` to `5` |
| Section header | `650` to `850` | `38` to `52` | `2.8` to `4` |
| Compact label | `420` to `650` | `28` to `40` | `2` to `3.2` |

## Design Rules

- Keep typing text short. Long sentences either shrink poorly or take too long to animate.
- Match the header tone to the project: calm for infrastructure, vivid for creative or AI demos.
- Put one animated header near the top, then use static section headings below.
- Use meaningful `alt` text that matches the visible message.
- Avoid placing several animated headers close together.

## GitHub Compatibility Notes

- Animated SVG headers render through standard Markdown image syntax and `<img>` tags.
- GitHub strips scripts and most custom CSS from Markdown, so keep animation inside the SVG.
- Raw GitHub URLs are best for public reusable assets.
- Relative paths are best when the asset lives in the same repository.

## Copy Checklist

- Choose an existing header or generate a custom one.
- Confirm the output path exists before embedding it.
- Keep the visible text and `alt` text aligned.
- Preview the header in GitHub light and dark themes.
