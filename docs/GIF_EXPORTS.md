# Local SVG to GIF Exports

SVG is the primary asset format in `readme-ux-kit`. GIF export exists as a local utility for users who need a downloadable motion preview or a fallback for a specific surface.

The repository should not commit curated GIF previews. Keep generated GIFs local unless a future change intentionally publishes a specific export.

## Policy

- Keep SVG as the first README copy format.
- Use GIF only as a fallback, preview, or export format.
- Do not replace source SVG assets with GIFs.
- Do not commit generated GIF exports by default.
- Prefer `output/gifs/` for local exports; it is ignored by Git.

## Local Studio Export

Run the Local Studio:

```bash
npm run app:dev
```

Open:

```text
http://127.0.0.1:8787
```

Select an asset, then use the GIF Export panel. The app can render either the original SVG or the edited SVG currently shown in the editor overlay.

The panel lets you choose:

- output folder;
- file name;
- duration;
- FPS;
- max width and height;
- background color;
- original or edited SVG source.

The default output folder is `output/gifs/`.

## CLI Export

Export a specific SVG:

```bash
npm run export:gif -- \
  --asset assets/loadings/loading_neural_synapse.svg \
  --output-dir output/gifs \
  --index-output output/gifs/index.json
```

Tune render settings:

```bash
npm run export:gif -- \
  --asset assets/loadings/loading_neural_synapse.svg \
  --duration-ms 2400 \
  --fps 15 \
  --max-width 720 \
  --max-height 280 \
  --min-width 240 \
  --min-height 120 \
  --background "#ffffff"
```

The CLI requires at least one `--asset` argument. Running it without assets will not generate a curated repository set.

Use `--background transparent` only when transparent GIF edges are acceptable. A solid background usually produces cleaner antialiasing.

## Dependencies

The exporter uses Chromium through Playwright so CSS and SVG animation are captured by a real browser. Pillow encodes the captured PNG frames into GIF files.

Install the Python tooling dependencies:

```bash
uv sync --project src
uv run --project src python -m playwright install chromium
```

## Output Rules

Local exports can produce:

| Path | Purpose |
| --- | --- |
| `output/gifs/**/*.gif` | Local GIF exports. |
| `output/gifs/index.json` | Optional local export metadata from the CLI. |
| `output/gifs/README.md` | Optional local export gallery from the CLI. |

These files are local output, not part of the repository generated-data contract.

## Quality Bar

Good GIF candidates:

- use flat or near-flat colors;
- have bold strokes and shapes;
- have motion that is visible at small sizes;
- avoid tiny text;
- avoid heavy blur, glow, and fine gradients.

Poor GIF candidates should remain SVG-only. The fallback should never make the asset look lower quality than the SVG preview.

## README Copy Pattern

Primary SVG embed:

```markdown
![Loading animation](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/loadings/loading_neural_synapse.svg)
```

Optional local GIF export after you generate and copy the file into your own project:

```markdown
![Loading animation GIF fallback](./assets/generated/loading_neural_synapse.gif)
```

For most GitHub READMEs, use the SVG unless you have a specific compatibility reason to use the GIF.
