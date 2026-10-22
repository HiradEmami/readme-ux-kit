# Accessibility Statement (WCAG 2.2 Level AA & EN 301 549)

`readme-ux-kit` is committed to digital accessibility and inclusive design across its 1,608 SVG assets, static browser showcase (`site/`), and Local Studio application (`src/app/`).

## Conformance Status

This repository targets conformance with:

- **Web Content Accessibility Guidelines (WCAG) 2.2 Level AA**
- **European Standard EN 301 549 V3.2.1** (European Accessibility Act Directive (EU) 2019/882)
- **WAI-ARIA 1.2 Authoring Practices**
- **Section 508 of the U.S. Rehabilitation Act**

## Implemented Accessibility Controls

| Standard / Criterion | Control Implemented | Verification |
| --- | --- | --- |
| WCAG 1.1.1 Non-Text Content | All 1,608 SVGs include `role="img"`, `aria-labelledby`, `<title>`, and `<desc>`. UI `<img>` tags include `alt` and `onerror` fallbacks. | `npm run check:svg:accessibility` |
| WCAG 2.4.1 Bypass Blocks | `<a class="skip-link" href="#main-content">Skip to main content</a>` is the first focusable element in both UIs. | `npm run check:site` |
| WCAG 2.1.1 / 2.4.7 Keyboard & Focus | All interactive controls and `.asset-card` items are operable via `Tab`, `Enter`, `Space`, and `Escape` with `>= 3:1` `:focus-visible` outlines. | `npm run check:site` |
| WAI-ARIA 1.2 Dialogs | Modals use `<dialog>` or `role="dialog" aria-modal="true"`, trap `Tab` focus while open, close on `Escape`, and restore trigger focus. | `npm run check:site` |
| WCAG 1.3.1 / 4.1.2 Landmarks & Labels | Semantic `<header>`, `<nav>`, `<main id="main-content">`, `<aside>`, and `<footer>` landmarks; explicit labels on all inputs. | `npm run check:site` |
| WCAG 4.1.3 Status Messages | Dynamic counters, command outputs, toast statuses, and crash banners use `role="status"` (`aria-live="polite"`) or `role="alert"`. | `npm run check:site` |
| WCAG 1.4.3 / 1.4.10 / 2.5.8 Contrast & Reflow | High-contrast dark palette, responsive single-column reflow down to `320px`, and `24x24 CSS px` minimum target sizes. | `npm run check:design-system` |
| WCAG 2.3.3 Motion & Vestibular Safety | `@media (prefers-reduced-motion: reduce)` and `matchMedia` listeners disable non-essential transitions; zero flashing `> 3 Hz`. | `npm run check:svg` |

## Assistive Technology & Browser Compatibility

- **Screen Readers**: NVDA, JAWS, Apple VoiceOver, and Orca with modern Chromium, Firefox, and WebKit browsers.
- **Keyboard-Only Navigation**: Press `?` anywhere in the Showcase or Local Studio (outside text inputs) to open the Keyboard Shortcut Cheat-Sheet.

## Known Limitations

- **GitHub README Host Constraints**: When SVGs are embedded inside GitHub Markdown via `<img>` or `[![alt](url)]`, GitHub's Camo proxy serves them as static/animated image resources without interactive internal DOM focus. Always preserve descriptive Markdown `alt` text when embedding assets.

## Feedback & Barrier Reporting

If you encounter an accessibility barrier:

1. Use the in-app **Report / Feedback** button (or press `?`) and select **Accessibility & Keyboard Navigation** to generate a PII-free Diagnostic Bundle.
2. Open an issue at <https://github.com/HiradEmami/readme-ux-kit/issues>.
