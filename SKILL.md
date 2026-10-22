---
name: readme-ux-kit
description: Design, validate, edit, and package accessible GitHub-native SVG assets, README templates, themes, and showcase artifacts in readme-ux-kit.
---

# readme-ux-kit Skill Instructions

Use this skill when creating or updating SVG assets, themes, recipes, Markdown documentation, the static browser showcase (`site/`), or the Local Studio (`src/app/`).

## Workflow

1. **Inspect Existing Assets & Standards**:
   - Review [`docs/VISUAL_STYLE.md`](docs/VISUAL_STYLE.md) and [`.codex/designer-session.md`](.codex/designer-session.md).
   - Ensure every SVG has `role="img"`, `aria-labelledby`, `<title>`, `<desc>`, and editor-ready `id` / `data-edit-id` / `data-edit-label` attributes.
2. **Optimize & Validate SVGs**:
   - Run `npm run optimize:svg`
   - Run `npm run check:svg` and `npm run check:svg:accessibility`
3. **Regenerate All Derived Catalogs & Previews**:
   - Run `npm run generate:previews`
   - Run `npm run generate:all-data`
   - Run `npm run build:pages`
4. **Run the Full Quality Gate**:
   - Run `npm run quality:gate`
   - Run `git diff --check`
