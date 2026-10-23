# Local Studio

`src/app/` is a local-only FastAPI wrapper around the repository modules. It serves a static HTML/CSS/JS interface for browsing assets, copying snippets, previewing safe SVG edits, exporting selected SVGs to GIF, and running whitelisted maintenance commands from the repo root.

This is not a hosted backend. Keep it bound to `127.0.0.1`.

## Install

From the repository root:

```bash
cd src
uv sync
cd ..
```

If you are not using `uv`, install `fastapi` and `uvicorn[standard]` into the Python environment you use to run the app.

## Run

```bash
npm run app:dev
```

Open:

```text
http://127.0.0.1:8787
```

For app development with reload:

```bash
npm run app:dev:reload
```

## Check

```bash
npm run check:app
```

The check compiles `src/app/` and runs dependency-light service self-tests. It does not require starting the web server.

## What The App Provides

| Area | Local route | Source |
| --- | --- | --- |
| Health | `/api/health` | Runtime status |
| Summary | `/api/summary` | Manifest, quality summary, generated data presence |
| Data files | `/api/data/{name}` | Whitelisted generated JSON files |
| Asset browser | `/api/assets` | `assets/manifest.json` or `site/data/assets.json` |
| Asset detail | `/api/assets/detail/{asset_path}` | SVG metadata plus source |
| Asset source | `/api/assets/source/{asset_path}` | Local SVG file |
| SVG editor | `/api/svg/edit` | `src/modules/editor/svg_editor.py` |
| GIF export | `/api/gif/export` | `src/modules/renderers/svg_to_gif.py` |
| GIF preview | `/api/gif/file/{gif_path}` | Generated local GIF files |
| Commands | `/api/run/{command}` | Whitelisted repo maintenance commands |

## Editor Interface

Select an asset, then use `Open Editor` to work in the overlay editor. The overlay uses generated SVG metadata for color controls, editable text fields, removable element toggles, animation speed controls, and an advanced JSON panel for direct operation payloads.

## GIF Export

Select an asset, choose an output folder and file name in the GIF Export panel, then export a browser-rendered GIF. The default output folder is `output/gifs/`, which is ignored and intended for local user output.

If the selected SVG has been edited in the overlay, enable `Use edited SVG` to render the edited markup instead of the original asset. The app returns a local preview plus Markdown and HTML snippets that point to the chosen repo-relative GIF path.

## Whitelisted Commands

The UI can run only these commands:

| Command id | Script |
| --- | --- |
| `generate-all-data` | `npm run generate:all-data` |
| `generate-previews` | `npm run generate:previews` |
| `check-all` | `npm run check:all` |
| `modules-check` | `npm run modules:check` |
| `modules-report` | `npm run modules:report` |
| `optimize-svg` | `npm run optimize:svg` |

## Local Safety Rules

- The server rejects non-localhost requests.
- Asset reads are constrained to SVG files under `assets/`.
- GIF output paths are constrained to folders inside the repository and outside `.git/`.
- Mutating commands are explicit and whitelisted.
- SVG edits are validated through the existing SVG validator before being returned.
- The app does not write edited SVG output to disk unless the user explicitly exports it as a GIF.

Run it only from a trusted checkout.
