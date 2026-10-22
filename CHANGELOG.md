# Changelog

All notable changes to `readme-ux-kit` are documented in this file following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See [`docs/CHANGELOG.md`](docs/CHANGELOG.md) for commit message conventions.

## [Unreleased]

### Added

- Added the 3D axonometric `assets/isometric/` category with 150 validated SVGs across 10 subcategories (`cloud-topology`, `data-pipelines`, `ai-systems`, `ci-cd-devops`, `security-zero-trust`, `observability-sre`, `developer-workstations`, `networking-mesh`, `storage-databases`, `platform-architecture`).
- Expanded 9 asset categories (`cards`, `charts`, `diagrams`, `dividers`, `file_headers`, `headers`, `icons`, `isometric`, `loadings`) with 50 new animated SVGs each, bringing the catalog to **1,608 validated SVG assets** (`460` static, `1,148` animated).
- Added in-app **Help Center & Keyboard Shortcut Cheat-Sheet (`?`)**, **Contextual Bug Reporter** (PII-free Diagnostic Bundle export), **User Feedback Widget**, **GDPR SAR Data Export**, **1-Click Local Cache Purge**, and **Runtime Error Boundary** to both `site/` and `src/app/static/`.
- Added [`ACCESSIBILITY.md`](ACCESSIBILITY.md), [`PRIVACY.md`](PRIVACY.md), [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md), [`ASSET_PROVENANCE.md`](ASSET_PROVENANCE.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`AGENTS.md`](AGENTS.md), [`SKILL.md`](SKILL.md), and RFC 9116 [`security.txt`](.well-known/security.txt).

### Security

- Enforced strict Content Security Policy (CSP), `Referrer-Policy`, `X-Content-Type-Options: nosniff`, and `X-Frame-Options: DENY` across static and local studio surfaces.
- Eliminated all `innerHTML` sinks in `site/app.js` and `src/app/static/app.js` in favor of safe DOM construction and `Blob` URLs.
- Added URL scheme/path allowlist validation (`isSafeAssetUrl`), prototype-pollution key rejection (`__proto__`, `constructor`, `prototype`), and byte-size caps (`512 KB` SVG / `64 KB` JSON).
- Added per-asset `byteLength` and `sha256` digests to [`assets/provenance.json`](assets/provenance.json) and [`ASSET_PROVENANCE.json`](ASSET_PROVENANCE.json).

## [1.0.0] - 2026-09-30

### Added

- Initial release of `readme-ux-kit` featuring curated SVG assets, 19 theme token systems, reusable Markdown components, README starter templates, static browser showcase, and Local Studio editor.
