# Accessibility Architecture & Conformance Guide

See the root [`ACCESSIBILITY.md`](../ACCESSIBILITY.md) for the formal WCAG 2.2 Level AA and EN 301 549 Accessibility Statement.

## Repository Accessibility Gateways

1. **SVG Asset Accessibility (`src/modules/generators/normalize_svg_accessibility.py`)**:
   - Enforces `role="img"`, `aria-labelledby`, `<title>`, and `<desc>` on all 1,608 SVG assets under [`assets/`](../assets/README.md).
2. **Showcase & Local Studio UI Accessibility (`src/modules/site/site_checks.py`)**:
   - Verifies skip links, landmark structure, labeled form controls, live regions, reduced-motion media queries, and modal focus restoration across [`site/index.html`](../site/index.html) and [`src/app/static/index.html`](../src/app/static/index.html).
