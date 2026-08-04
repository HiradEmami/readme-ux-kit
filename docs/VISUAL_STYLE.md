# Visual Style Guide

This guide keeps `readme-ux-kit` assets consistent, readable, and safe to copy into GitHub READMEs.

## Core Principles

- Prefer clarity over decoration.
- Use animation to guide attention, not distract from content.
- Keep assets self-contained and GitHub-compatible.
- Make assets useful in real README sections, not just visually interesting in isolation.
- Design for both quick browsing and direct copy/paste reuse.

## Color Guidance

| Role | Suggested colors | Use |
| --- | --- | --- |
| Success | `#22c55e`, `#34d399` | Passing checks, healthy systems, completed work. |
| Info | `#22d3ee`, `#38bdf8`, `#60a5fa` | Links, neutral technical states, scans, data flows. |
| Warning | `#f59e0b`, `#fbbf24` | Pending work, warnings, caution states. |
| Danger | `#ef4444`, `#fb365d`, `#fb7185` | Security, failed checks, destructive states. |
| Premium/accent | `#8b5cf6`, `#a78bfa`, `#f472b6` | Highlights and strong visual identity. |
| Dark base | `#020617`, `#05070d`, `#0f172a` | Backgrounds and panels. |

Avoid using red or amber as decoration when the asset does not represent warning or risk.

## Animation Guidance

Good animation:

- loops cleanly
- has a clear purpose
- stays subtle in dense README sections
- works without external scripts
- avoids flashing or rapid contrast changes

Avoid:

- very fast blinking
- large moving elements crossing over text
- animations that obscure labels
- multiple unrelated animations in the same small asset

## Layout Guidance

- Keep important text away from animated decorations.
- Leave clear padding around edges to avoid clipping.
- Prefer stable dimensions such as `850x90` for file headers and headers.
- Use `viewBox` on every SVG.
- Keep the main label readable at GitHub-rendered sizes.
- Do not rely on external fonts; use common fallback stacks.

## README Compatibility

GitHub strips or ignores many web features. Assets and snippets should avoid:

- JavaScript
- external CSS
- external image references inside SVGs
- custom web fonts
- unsupported layout dependencies

Allowed patterns:

- inline SVG gradients, filters, masks, and CSS animation
- standard Markdown image syntax
- GitHub-compatible HTML such as `<img>`, `<p>`, `<a>`, `<details>`, and `<summary>`

## Accessibility

- Add meaningful `aria-label` values to standalone SVGs when practical.
- Keep contrast high for text-based SVGs.
- Avoid relying on color alone for status meaning when a label can clarify it.
- Avoid aggressive flashing animation.

## Quality Checklist

- [ ] It has a clear use case.
- [ ] It has a descriptive filename.
- [ ] It includes a `viewBox`.
- [ ] It parses as XML.
- [ ] It has no `<script>`.
- [ ] It has no external `href` or `src` references.
- [ ] Text and animation do not overlap.
- [ ] It renders cleanly in the generated preview.
- [ ] It fits the category style.

Run:

```bash
npm run check:all
```
