# Known Limitations

`readme-ux-kit` is designed for GitHub README rendering. That makes it easy to copy and reuse, but it also means the project inherits GitHub Markdown, SVG, badge, and raw URL constraints.

## GitHub Markdown Rendering

- GitHub strips or ignores many custom HTML attributes and styles.
- JavaScript does not run in README files.
- External CSS is not supported.
- Layout options are limited to Markdown, tables, images, and a small set of allowed HTML tags.
- Wide tables can be hard to read on smaller screens.
- GitHub rendering can differ from local Markdown previewers.

Recommended approach:

- Use standard Markdown first.
- Use GitHub-compatible HTML only when needed, such as `<p>`, `<img>`, `<a>`, `<details>`, and `<summary>`.
- Keep copied sections narrow and easy to scan.

## SVG Animation

- SVG animation support can vary across browsers, GitHub surfaces, and user settings.
- Motion-heavy assets may distract from README content.
- Some users prefer reduced motion.
- Very small rendered sizes can make animation look noisy.
- Text embedded inside SVGs is not easily localized or edited by downstream users.

Recommended approach:

- Prefer subtle loops.
- Use static assets for dense documentation.
- Keep animated heroes, loaders, and dividers purposeful.
- Check important visuals in GitHub light and dark mode.

## GIF Fallbacks

- GIFs lose SVG scalability and usually produce larger files.
- GIF color palettes are limited, so gradients and glow effects can band.
- Transparent GIF edges can look rough because GIF transparency is not full alpha.
- Browser-rendered GIF capture requires Playwright, Chromium, and Pillow.

Recommended approach:

- Keep SVG as the primary copy format.
- Generate GIFs locally only when a specific README or preview surface needs one.
- Use a solid background when visual polish matters.
- Keep exported GIFs out of the committed repository unless you explicitly intend to publish them.

## External Badges

- Shields and workflow badges depend on third-party or GitHub-hosted endpoints.
- Badges can fail, cache stale values, or expose incorrect status if URLs are copied without updating placeholders.
- Some examples use placeholder paths such as `OWNER`, `REPO`, `PACKAGE_NAME`, or `ci.yml`.

Recommended approach:

- Link badges to verifiable pages.
- Replace every placeholder before publishing.
- Keep badge rows short and factual.
- Do not use badges for claims you do not maintain.

## Raw GitHub URLs

- Raw GitHub URLs are convenient for previews and direct copy/paste, but they depend on branch names and file paths.
- Renaming or deleting an asset can break downstream READMEs that embed it.
- The default examples use the `master` branch.

Recommended approach:

- Copy assets into your own repository when long-term stability matters.
- Use relative paths for project-local assets.
- Follow the asset deprecation policy before renaming or removing files.

## Generated Preview Pages

- Files under `previews/assets/` are generated output.
- They should not be edited by hand.
- Preview pages are optimized for GitHub browsing, not for advanced search or filtering.

Recommended approach:

- Change `src/modules/generators/generate_asset_previews.py` when preview structure needs to change.
- Run `npm run generate:previews` after asset changes.
- Run `npm run check:previews` before committing.

## Static Gallery Asset Delivery

- The committed `site/` directory contains the static shell and generated data, but not duplicate copies of `assets/`.
- GitHub Pages deployment runs `npm run build:pages` and uploads `build/pages/`, which includes all manifest SVGs under a same-origin `assets/` directory.
- To preview the source shell, serve the repository root and open `/site/`.
- To serve a standalone document root, run `npm run build:pages` and serve `build/pages/`.
- Gallery images, editor sources, and downloads use bundled or repository-local SVGs. They do not depend on unauthenticated raw GitHub access.
- Copyable README snippets may still contain raw GitHub URLs; those URLs require the repository and referenced revision to be publicly readable.

## Generated Module Data

- Files under `site/data/`, `site/reports/`, `site/packages/`, `assets/manifest.json`, `assets/provenance.json`, and `themes/index.json` are generated from repository source files.
- Generated JSON is designed for a frontend-only static site and local quality checks, not as a public API with backward compatibility guarantees.
- Some reports intentionally emit warnings for valid but imperfect docs, such as wide tables or duplicate subsection anchors.

Recommended approach:

- Run `npm run generate:all-data` after source changes.
- Run `npm run modules:check` for generated data freshness.
- Treat `docs/MODULES.md` as the source of truth for module outputs and focused commands.

## Local Studio

- `src/app/` is intended for local repository maintenance, not public hosting.
- The app has no authentication layer because it is expected to bind to `127.0.0.1`.
- Command execution is intentionally limited to a small whitelist.
- Edited SVGs are returned for copy/paste; the app does not save edited SVGs to disk.

Recommended approach:

- Keep the server on localhost.
- Run it only from a trusted checkout.
- Use the static future GitHub Pages lane for public showcases, not `src/app/`.

## Asset Quality

- The library is broad and visual QA is still an ongoing task.
- Some older assets may use different visual styles than newer additions.
- Some existing filenames may contain typos retained for raw URL compatibility.

Recommended approach:

- Browse generated previews before choosing assets.
- Prefer curated bundles and recipes when you want a faster path.
- Report visual clipping, distracting animation, or naming issues through focused issues or pull requests.
