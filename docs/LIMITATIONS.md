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

## Asset Quality

- The library is broad and visual QA is still an ongoing task.
- Some older assets may use different visual styles than newer additions.
- Some existing filenames may contain typos retained for raw URL compatibility.

Recommended approach:

- Browse generated previews before choosing assets.
- Prefer curated bundles and recipes when you want a faster path.
- Report visual clipping, distracting animation, or naming issues through focused issues or pull requests.

