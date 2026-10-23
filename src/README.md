# readme-ux-kit Tooling

This directory contains the Python tooling for `readme-ux-kit`.

| Path | Purpose |
| --- | --- |
| [`modules/`](./modules/) | Generators, validators, analyzers, indexes, reports, packs, release checks, and shared helpers. |
| [`app/`](./app/README.md) | Local-only browser studio for asset browsing, SVG edit previews, user GIF exports, generated data, and whitelisted checks. |

From the repository root:

```bash
npm run generate:all-data
npm run check:all
npm run app:dev
npm run export:gif -- --asset assets/loadings/loading_spinner_arc.svg
```
