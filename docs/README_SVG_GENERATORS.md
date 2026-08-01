# README SVG Generators

The generator toolkit creates self-contained SVGs for README headers, status sections, cards, dividers, diagrams, and profile blocks.

## Available Generators

| Generator | Use |
| --- | --- |
| [`generate_typing_svg.py`](../src/modules/generators/generate_typing_svg.py) | Animated typing headers. |
| [`generate_readme_svg.py`](../src/modules/generators/generate_readme_svg.py) | Multi-preset generator for common README visuals. |

## Multi-Preset Generator

`generate_readme_svg.py` supports 12 presets:

| Preset | Best for |
| --- | --- |
| `architecture` | Simple client-service-data diagrams. |
| `badge-strip` | Custom badge-like status rows. |
| `divider` | Animated section separators. |
| `feature-grid` | Compact feature cards. |
| `metric-card` | KPI, coverage, score, or release metrics. |
| `profile-card` | GitHub profile and maintainer cards. |
| `progress` | Percent-complete bars. |
| `quote` | Project principle or positioning callouts. |
| `roadmap` | Step or milestone flows. |
| `status-panel` | Operational status summaries. |
| `terminal` | CLI-style command blocks. |
| `wave-banner` | Hero and section banners. |

## Examples

### Wave Banner

```bash
python src/modules/generators/generate_readme_svg.py \
  --preset wave-banner \
  --title "README UX KIT" \
  --subtitle "Copyable assets, templates, and components" \
  --primary "#22d3ee" \
  --secondary "#8b5cf6" \
  --width 900 \
  --height 180 \
  --output assets/headers/animated/readme_ux_wave.svg
```

### Status Panel

```bash
python src/modules/generators/generate_readme_svg.py \
  --preset status-panel \
  --title "Project Health" \
  --items "build:passing|previews:current|svg:validated" \
  --output status_panel.svg
```

### Progress Bar

```bash
python src/modules/generators/generate_readme_svg.py \
  --preset progress \
  --label "release readiness" \
  --value 88 \
  --output release_readiness.svg
```

### Architecture Diagram

```bash
python src/modules/generators/generate_readme_svg.py \
  --preset architecture \
  --title "Service Flow" \
  --primary "#38bdf8" \
  --secondary "#22c55e" \
  --output architecture.svg
```

## Validation

Run generator self-tests:

```bash
python src/modules/generators/generate_readme_svg.py --self-test
```

After adding generated SVGs to the asset library:

```bash
npm run optimize:svg
npm run generate:previews
npm run check:all
```

Generated SVGs should still follow the same asset rules as hand-authored SVGs: valid `viewBox`, no scripts, no external resources, and readable output in GitHub light and dark modes.
