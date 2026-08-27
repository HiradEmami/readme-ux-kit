# Cyberpunk Colors

Color guidance for the cyberpunk README theme. Use this file as a palette reference when creating new SVGs, badges, tables, and section art for the theme.

## Core Palette

| Token | Hex | Usage |
| --- | --- | --- |
| `void` | `#05070d` | Page-level dark background, deep panels, negative space |
| `panel` | `#0b1020` | Tables, grouped content, secondary backgrounds |
| `grid` | `#172033` | Lines, borders, circuit strokes, low-emphasis UI |
| `cyan` | `#22d3ee` | Primary neon accent, links, scan lines |
| `blue` | `#38bdf8` | Secondary accent, status highlights |
| `violet` | `#8b5cf6` | High-energy glow, active states, premium accents |
| `magenta` | `#f472b6` | Alert accents, hover states, rare emphasis |
| `red` | `#fb365d` | Danger states, security warnings, failure signals |
| `amber` | `#fbbf24` | Warning states, pending tasks, attention markers |
| `green` | `#34d399` | Success states, healthy systems, completed checks |
| `text` | `#e5f4ff` | Primary foreground text inside SVG assets |
| `muted` | `#94a3b8` | Secondary labels and low-priority annotations |

## Status Mapping

| State | Primary | Secondary | Recommended asset family |
| --- | --- | --- | --- |
| Online | `#34d399` | `#22d3ee` | `assets/icons/status/`, `assets/icons/data-ai/` |
| Running | `#38bdf8` | `#8b5cf6` | `assets/loadings/`, `assets/dividers/animated/` |
| Warning | `#fbbf24` | `#fb923c` | `assets/icons/status/icon_warning.svg` |
| Danger | `#fb365d` | `#f472b6` | `assets/icons/status/icon_danger.svg` |
| Deprecated | `#94a3b8` | `#475569` | `assets/icons/status/icon_deprecated.svg` |

## Contrast Rules

- Keep body text close to `#e5f4ff` when it appears inside dark SVGs.
- Use cyan and blue for primary reading paths.
- Reserve red and magenta for real alerts, not general decoration.
- Avoid placing violet text on dark blue without a glow or light outline.
- Keep table borders subtle; the theme should feel technical, not noisy.

## Suggested Gradients

```css
--cyber-scan: linear-gradient(90deg, #22d3ee, #8b5cf6, #f472b6);
--cyber-danger: linear-gradient(90deg, #fb365d, #fbbf24);
--cyber-system: linear-gradient(90deg, #34d399, #22d3ee, #38bdf8);
--cyber-depth: linear-gradient(180deg, #05070d, #0b1020);
```

## Usage Notes

The cyberpunk theme works best when the README has a strong information hierarchy: a single visual header, short tables, compact status rows, and dividers between major sections. Use motion sparingly in dense documents so the important signals remain readable.
