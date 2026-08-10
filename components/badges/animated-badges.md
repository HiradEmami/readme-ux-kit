# Animated Badges

> Maturity: `draft`

Motion-forward badge patterns for READMEs that need a little energy while staying compatible with GitHub Markdown. Use animated badges sparingly: they are strongest when they highlight one or two live signals, not when every status indicator is moving.

## Animated Header Row

```markdown
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

<p align="center">
  <img alt="Project activity" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/loadings/loading_bouncing_dots.svg" width="80">
</p>
```

This pattern keeps primary project metadata as stable Shields.io badges and reserves motion for a single supporting asset.

## Live Typing Badge

Use the repository typing SVG generator when you want a custom animated line above or below your badge row.

```bash
python src/modules/generators/generate_typing_svg.py \
  --text "Fast builds. Clear docs. Reliable releases." \
  --text-color "#38bdf8" \
  --font-size 42 \
  --width 900 \
  --duration 4 \
  --output assets/headers/animated/status_typing.svg
```

Then embed it:

```markdown
<p align="center">
  <img alt="Fast builds. Clear docs. Reliable releases." src="./assets/headers/animated/status_typing.svg">
</p>
```

## Motion Status Strip

```markdown
<p align="center">
  <img alt="Loading" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/loadings/loading_dual_ring_reactor.svg" width="28">
  <a href="https://github.com/OWNER/REPO/actions">
    <img alt="Pipeline" src="https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=flat-square&label=pipeline&color=16a34a">
  </a>
  <a href="https://github.com/OWNER/REPO/releases">
    <img alt="Latest release" src="https://img.shields.io/github/v/release/OWNER/REPO?style=flat-square&label=release&color=2563eb">
  </a>
  <img alt="Loading" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/loadings/loading_dual_ring_reactor.svg" width="28">
</p>
```

## Release Pulse

```markdown
<p align="center">
  <a href="https://github.com/OWNER/REPO/releases">
    <img alt="Latest release" src="https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=latest&color=7c3aed">
  </a>
  <img alt="Release pulse" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/loadings/loading_double_pulse_ring.svg" width="36">
  <a href="https://github.com/OWNER/REPO/commits/main">
    <img alt="Last commit" src="https://img.shields.io/github/last-commit/OWNER/REPO?style=for-the-badge&label=updated&color=0f766e">
  </a>
</p>
```

## Animated Capability Panel

Use this when the badges are part of a polished hero block.

```html
<div align="center">
  <img alt="System online" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/animated/header_scanning_status.svg">
  <br>
  <a href="https://github.com/OWNER/REPO/actions">
    <img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=for-the-badge&label=build&color=16a34a">
  </a>
  <a href="https://github.com/OWNER/REPO/releases">
    <img alt="Release version" src="https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=release&color=2563eb">
  </a>
  <a href="https://github.com/OWNER/REPO/issues">
    <img alt="Open issues" src="https://img.shields.io/github/issues/OWNER/REPO?style=for-the-badge&label=issues&color=f59e0b">
  </a>
</div>
```

If the referenced animated header does not exist in your repository, generate one with `src/modules/generators/generate_typing_svg.py` or use one of the existing assets under `assets/headers/animated/`.

## Motion Guidelines

- Animate only one visual element in the badge cluster whenever possible.
- Do not place multiple spinners beside critical status badges; it can make stable information feel uncertain.
- Keep animated assets small: `24` to `96` pixels wide usually works best.
- Always include meaningful `alt` text. If the animation is decorative, use concise context such as `Project activity`.
- Prefer SVG animation assets over GIFs for crisp rendering and smaller file sizes.

## GitHub Compatibility Notes

- GitHub Markdown supports image-based SVG animation in normal `img` and Markdown image syntax.
- Custom `<style>` blocks, external scripts, and most inline CSS animation are stripped or ignored.
- Animated SVGs hosted from raw GitHub URLs work well for public repositories.
- For private repositories, copy the asset into the same repository and use a relative path.

## Copy Checklist

- Replace `OWNER`, `REPO`, `main`, and workflow filenames.
- Confirm every raw asset URL exists before publishing.
- Keep the moving element below or beside the badge row, not between every badge.
- Check the README in both light and dark GitHub themes.
