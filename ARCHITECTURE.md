# Architecture & System Design

`readme-ux-kit` is a deterministic, local-first GitHub README design system, SVG asset catalog, static browser showcase, and local FastAPI studio.

## 1. High-Level System Architecture

```mermaid
flowchart TD
  subgraph Sources["Human-Authored Sources"]
    SVG["assets/**/*.svg (1,608 SVGs)"]
    DOCS["docs/*.md & themes/*/tokens.json"]
    TEMPLATES["templates/** & components/**"]
  end

  subgraph Pipeline["Deterministic Python Module Pipeline (src/modules/)"]
    VALIDATORS["Validators & Accessibility Normalizer"]
    GENERATORS["Preview, Manifest & Editor Generators"]
    INDEXERS["Search, Tag, Theme, Recipe & Provenance Indexers"]
    REPORTS["Compatibility, Smoke Render & Quality Reports"]
  end

  subgraph Artifacts["Committed Generated Artifacts"]
    PREVIEWS["previews/assets/**/*.md"]
    MANIFEST["assets/manifest.json & assets/provenance.json"]
    SITEDATA["site/data/*.json & site/reports/quality-report.md"]
  end

  subgraph Surfaces["Interactive User Surfaces"]
    PAGES["Static Browser Showcase (site/ -> build/pages/)"]
    STUDIO["Local Studio FastAPI App (src/app/)"]
  end

  SVG --> VALIDATORS
  DOCS --> VALIDATORS
  TEMPLATES --> VALIDATORS
  VALIDATORS --> GENERATORS
  GENERATORS --> INDEXERS
  INDEXERS --> REPORTS
  REPORTS --> PREVIEWS
  REPORTS --> MANIFEST
  REPORTS --> SITEDATA
  MANIFEST --> PAGES
  SITEDATA --> PAGES
  MANIFEST --> STUDIO
  SITEDATA --> STUDIO
```

## 2. Interactive Surface Request & Security Flow

```mermaid
flowchart LR
  USER["User Browser"]
  CSP["CSP & URL Allowlist Gate"]
  SHOWCASE["Static Showcase (site/app.js)"]
  FASTAPI["LocalLoopback Middleware (127.0.0.1 only)"]
  SERVICES["Service Layer (src/app/services.py)"]
  EDITOR["Safe XML/SVG Editor (src/modules/editor/svg_editor.py)"]

  USER --> CSP
  CSP --> SHOWCASE
  CSP --> FASTAPI
  FASTAPI --> SERVICES
  SERVICES --> EDITOR
```

## 3. Directory & Module Boundaries

| Layer | Path | Responsibility |
| --- | --- | --- |
| Curated SVG Library | [`assets/`](assets/README.md) | 1,608 self-contained, accessible SVG assets across 19 categories. |
| Generated Markdown Previews | [`previews/assets/`](previews/assets/README.md) | Category summaries and full per-group preview galleries. |
| Static Browser Showcase | [`site/`](site/index.html) | Zero-dependency static web app for searching, filtering, and editing SVGs in-browser. |
| Local Studio Server | [`src/app/`](src/app/api.py) | Loopback-only FastAPI app wrapping `src/modules` for local editing and GIF export. |
| Core Python Tooling | [`src/modules/`](docs/MODULES.md) | Deterministic generators, analyzers, indexers, schemas, and quality validators. |
| Themes, Recipes & Templates | [`themes/`](themes/README.md), [`templates/`](templates/README.md) | 19 color/token themes, composition recipes, and starter README layouts. |

## 4. Quality & Release Verification Gate

Run the complete deterministic verification suite with a single command:

```bash
npm run quality:gate
```
