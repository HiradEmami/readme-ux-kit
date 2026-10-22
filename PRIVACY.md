# Privacy & Data Governance Policy (GDPR / ePrivacy / CCPA)

`readme-ux-kit` is engineered on a **Privacy-by-Default, Local-First, Zero-Telemetry** architecture in accordance with **GDPR (Regulation (EU) 2016/679 Art. 15, 17, 20, 25)**, the **EU ePrivacy Directive (Art. 5(3))**, and **CCPA/CPRA**.

## 1. Zero Illicit Tracking & Telemetry

- **No Tracking Cookies**: Neither the static showcase (`site/`) nor the Local Studio (`src/app/`) sets any first-party or third-party HTTP cookies.
- **No Analytics or Behavioral Fingerprinting**: Zero external analytics scripts, telemetry beacons, or fingerprinting collectors are loaded or executed.
- **Strict Content Security Policy**: Enforced via `<meta http-equiv="Content-Security-Policy">` and FastAPI HTTP response headers (`default-src 'self'; connect-src 'self'; object-src 'none'`).

## 2. Complete Client Storage Inventory

Every client-side storage key used by the application is inventoried below:

| Storage Mechanism | Exact Key Name | Purpose | Schema / Example | Retention Lifecycle |
| --- | --- | --- | --- | --- |
| `localStorage` | `readmeUxKitFavorites` | Stores user-favorited SVG asset paths in `site/app.js`. | JSON array of asset path strings (`["assets/cards/features/card.svg"]`). | Retained locally until user unchecks favorites or clicks **Purge Local Cache**. |
| `sessionStorage` | *(None)* | No `sessionStorage` keys are written by default. | Cleared on **Purge Local Cache**. | Session-scoped only. |
| `IndexedDB` | *(None)* | Not used. | N/A | N/A |
| HTTP Cookies | *(None)* | Not used. | N/A | N/A |

## 3. External Network & Subprocessor Disclosure

| Surface | Default Outbound Network Requests | Optional User-Triggered Links | Offline / Self-Hosted Operation |
| --- | --- | --- | --- |
| Static Showcase (`site/`) | **Zero external requests**. Loads local `./styles.css`, `./app.js`, `./data/*.json`, and `./assets/**/*.svg`. | Clicking external links (`Source`, `Preview`, `GitHub Issue Tracker`) opens `https://github.com/HiradEmami/readme-ux-kit` in a new tab. | Stage with `npm run build:pages` and serve `build/pages/` from any offline HTTP server. |
| Local Studio (`src/app/`) | **Zero external requests**. Binds strictly to loopback (`127.0.0.1` / `localhost`). | Copyable Markdown snippets reference `https://raw.githubusercontent.com/...` for GitHub README embedding. | Run `npm run app:dev` for 100% offline local operation. |

## 4. Data Subject Rights (GDPR Art. 15, 17 & 20)

Both the Static Showcase and Local Studio provide built-in, 1-click user controls in the footer and in the **Report / Feedback (`?`)** modal:

1. **Right of Access & Data Portability (`GDPR Art. 15 & 20`)**: Click **Export My Data (JSON)** to download a versioned, machine-readable JSON archive (`readme-ux-kit-user-data-export.json`) containing your complete `localStorage` inventory and active workspace preferences.
2. **Right to Erasure / Right to be Forgotten (`GDPR Art. 17`)**: Click **Purge Local Cache & Reset All Data** to immediately delete `readmeUxKitFavorites`, clear `localStorage` and `sessionStorage`, revoke temporary `Blob` preview URLs, and restore default in-memory state.
