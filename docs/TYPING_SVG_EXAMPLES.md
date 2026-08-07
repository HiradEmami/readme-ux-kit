# Typing SVG Examples

`generate_typing_svg.py` creates a self-contained animated SVG header with a type-on mask and blinking cursor. It is useful for README titles, status headers, file headers, and terminal-style project intros.

For other generated README visuals such as status panels, progress bars, dividers, roadmap flows, profile cards, and architecture diagrams, see [README SVG generators](./README_SVG_GENERATORS.md).

## Basic Usage

```bash
python src/modules/generators/generate_typing_svg.py \
  --text "Build faster" \
  --output typing.svg
```

Embed the generated file:

```markdown
![Build faster](./typing.svg)
```

## Recommended Sizes

| Use case | Width | Font size | Duration | Notes |
| --- | --- | --- | --- | --- |
| Short title | `650` | `72` | `2.8` | Good for one or two words. |
| Project header | `850` | `72` | `3.5` | Default README hero format. |
| Long section title | `1000` | `60` | `4.0` | Use smaller text for longer phrases. |
| Compact badge/header | `520` | `48` | `2.6` | Useful inside dense docs. |

## Project Header

```bash
python src/modules/generators/generate_typing_svg.py \
  --text "README UX KIT" \
  --text-color "#38bdf8" \
  --font-size 72 \
  --width 850 \
  --duration 3.4 \
  --steps 32 \
  --output assets/headers/animated/readme_ux_kit_typing.svg
```

## Terminal Style

```bash
python src/modules/generators/generate_typing_svg.py \
  --text "> SYSTEM ONLINE" \
  --text-color "#22c55e" \
  --font-size 64 \
  --width 850 \
  --duration 3.2 \
  --steps 28 \
  --output assets/headers/animated/system_online_typing.svg
```

## Warning Header

```bash
python src/modules/generators/generate_typing_svg.py \
  --text "> SECURITY REVIEW" \
  --text-color "#fb365d" \
  --font-size 62 \
  --width 900 \
  --duration 3.6 \
  --steps 34 \
  --output assets/file_headers/security_review_typing.svg
```

## Tips

- Keep text short enough to fit the configured width.
- Use uppercase for terminal-style headers.
- Increase `--steps` for longer text so the typing motion feels smoother.
- Use color intentionally: green for healthy, cyan/blue for neutral technical states, amber for warnings, red for danger.
- Commit generated SVGs only when they are intended to be part of the asset library.

## Validation

After creating a reusable asset, run:

```bash
npm run check:svg
npm run generate:previews
npm run check:previews
```
