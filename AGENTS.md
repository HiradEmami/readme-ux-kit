# AGENTS.md — Agentic Engineering & Quality Gate Contract

This document defines the operating rules, repository layout, regeneration pipelines, and verification gates for autonomous coding agents working in `readme-ux-kit`.

## 1. Repository Overview

- **Mission**: A GitHub-native README design system with **1,608 validated SVG assets** across **19 categories**, **19 theme token systems**, reusable Markdown components, README starter templates, a static browser showcase (`site/`), and a loopback FastAPI Local Studio (`src/app/`).
- **Authoritative Scripts**: Defined in [`package.json`](package.json) and [`src/pyproject.toml`](src/pyproject.toml).

## 2. Non-Negotiable Operating Invariants

1. **Never Hand-Edit Generated Artifacts**:
   - Generated files include `previews/assets/**`, `assets/manifest.json`, `assets/provenance.json`, `ASSET_PROVENANCE.json`, `site/data/*.json`, `site/svg-contact-sheet.html`, `site/packages/README.md`, and `site/reports/quality-report.md`.
   - Always update the source SVG, Markdown, or Python generator under `src/modules/` and run `npm run generate:previews` and `npm run generate:all-data`.
2. **SVG Technical & Accessibility Standard**:
   - Every SVG under `assets/` must be valid UTF-8 XML with `xmlns="http://www.w3.org/2000/svg"`, a positive 4-number `viewBox`, `role="img"`, `aria-labelledby`, `<title>`, and `<desc>`.
   - Zero `<script>`, zero external `href`/`src` URLs, zero `<foreignObject>`, and zero embedded raster images.
3. **Static Showcase Boundary (`site/`)**:
   - `site/index.html` and `site/app.js` must remain 100% static-host compatible and must never reference local FastAPI routes, loopback addresses, or root-relative `/...` asset paths.
4. **Zero `innerHTML` & Strict Security**:
   - Use safe DOM construction (`document.createElement`, `document.createElementNS`, `replaceChildren`) and `Blob` URLs. Never introduce `innerHTML`, `eval`, or unvalidated URLs.

## 3. Standard Agent Regeneration & Verification Workflow

Run these commands after any asset, documentation, or code change:

```bash
npm run optimize:svg
npm run generate:previews
npm run generate:all-data
npm run build:pages
npm run quality:gate
git diff --check
```
