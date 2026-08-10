# Neon Badges

> Maturity: `experimental`

High-impact badge sets for READMEs that need a more expressive visual tone: developer tools, AI projects, creative coding, portfolio repositories, demos, and experimental systems.

Neon badges should still carry useful information. Treat the glow and color as presentation, not a substitute for status, version, platform, or capability.

## Cyber Product Row

```markdown
[![Status](https://img.shields.io/badge/status-online-00f5d4?style=for-the-badge&labelColor=111827)](https://github.com/OWNER/REPO)
[![Version](https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=version&color=7c3aed&labelColor=111827)](https://github.com/OWNER/REPO/releases)
[![Stack](https://img.shields.io/badge/stack-TypeScript-38bdf8?style=for-the-badge&labelColor=111827)](https://www.typescriptlang.org/)
[![Mode](https://img.shields.io/badge/mode-realtime-f97316?style=for-the-badge&labelColor=111827)](https://github.com/OWNER/REPO)
[![License](https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&color=f472b6&labelColor=111827)](../../LICENSE)
```

Preview:

[![Status](https://img.shields.io/badge/status-online-00f5d4?style=for-the-badge&labelColor=111827)](https://github.com/OWNER/REPO)
[![Version](https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=version&color=7c3aed&labelColor=111827)](https://github.com/OWNER/REPO/releases)
[![Stack](https://img.shields.io/badge/stack-TypeScript-38bdf8?style=for-the-badge&labelColor=111827)](https://www.typescriptlang.org/)
[![Mode](https://img.shields.io/badge/mode-realtime-f97316?style=for-the-badge&labelColor=111827)](https://github.com/OWNER/REPO)
[![License](https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&color=f472b6&labelColor=111827)](../../LICENSE)

## AI Lab Row

```markdown
[![Agent](https://img.shields.io/badge/agent-active-00f5d4?style=for-the-badge&labelColor=0b1020)](https://github.com/OWNER/REPO)
[![Models](https://img.shields.io/badge/models-evaluated-8b5cf6?style=for-the-badge&labelColor=0b1020)](./reports)
[![Latency](https://img.shields.io/badge/latency-p95_420ms-22d3ee?style=for-the-badge&labelColor=0b1020)](./benchmarks)
[![Eval](https://img.shields.io/badge/eval-regression_safe-a3e635?style=for-the-badge&labelColor=0b1020)](./evals)
[![Dataset](https://img.shields.io/badge/data-versioned-f59e0b?style=for-the-badge&labelColor=0b1020)](./data)
```

**Preview:**

[![Agent](https://img.shields.io/badge/agent-active-00f5d4?style=for-the-badge&labelColor=0b1020)](https://github.com/OWNER/REPO)
[![Models](https://img.shields.io/badge/models-evaluated-8b5cf6?style=for-the-badge&labelColor=0b1020)](./reports)
[![Latency](https://img.shields.io/badge/latency-p95_420ms-22d3ee?style=for-the-badge&labelColor=0b1020)](./benchmarks)
[![Eval](https://img.shields.io/badge/eval-regression_safe-a3e635?style=for-the-badge&labelColor=0b1020)](./evals)
[![Dataset](https://img.shields.io/badge/data-versioned-f59e0b?style=for-the-badge&labelColor=0b1020)](./data)

## Developer Tool Row

```markdown
[![CLI](https://img.shields.io/badge/cli-ready-00f5d4?style=flat-square&labelColor=111827)](https://github.com/OWNER/REPO)
[![Install](https://img.shields.io/npm/v/PACKAGE_NAME?style=flat-square&label=npm&color=38bdf8&labelColor=111827)](https://www.npmjs.com/package/PACKAGE_NAME)
[![Downloads](https://img.shields.io/npm/dm/PACKAGE_NAME?style=flat-square&label=downloads&color=8b5cf6&labelColor=111827)](https://www.npmjs.com/package/PACKAGE_NAME)
[![DX](https://img.shields.io/badge/dx-polished-f472b6?style=flat-square&labelColor=111827)](https://github.com/OWNER/REPO)
```

**Preview:**

[![CLI](https://img.shields.io/badge/cli-ready-00f5d4?style=flat-square&labelColor=111827)](https://github.com/OWNER/REPO)
[![Install](https://img.shields.io/npm/v/PACKAGE_NAME?style=flat-square&label=npm&color=38bdf8&labelColor=111827)](https://www.npmjs.com/package/PACKAGE_NAME)
[![Downloads](https://img.shields.io/npm/dm/PACKAGE_NAME?style=flat-square&label=downloads&color=8b5cf6&labelColor=111827)](https://www.npmjs.com/package/PACKAGE_NAME)
[![DX](https://img.shields.io/badge/dx-polished-f472b6?style=flat-square&labelColor=111827)](https://github.com/OWNER/REPO)


## HTML Glow Shell

GitHub strips most custom CSS from Markdown, but you can use a table wrapper to give neon badges stronger visual placement without relying on unsafe styles.

```html
<table>
  <tr>
    <td>
      <a href="https://github.com/OWNER/REPO/releases">
        <img alt="Version" src="https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=version&color=7c3aed&labelColor=111827">
      </a>
      <a href="https://github.com/OWNER/REPO/actions">
        <img alt="Build" src="https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=for-the-badge&label=build&color=00f5d4&labelColor=111827">
      </a>
      <a href="../../LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&color=f472b6&labelColor=111827">
      </a>
    </td>
  </tr>
</table>
```

## Palette Recipes

```text
Aurora:      00f5d4, 38bdf8, 8b5cf6, f472b6
Circuit:     a3e635, 22c55e, 14b8a6, 0f172a
Synthwave:   f97316, f43f5e, a855f7, 06b6d4
Terminal:    22c55e, 84cc16, eab308, 111827
```

Use `labelColor=111827` or `labelColor=0b1020` to anchor bright colors against a dark label block.

## Design Rules

- Keep neon rows short. Bright badges lose impact when the row becomes noisy.
- Use vivid colors for categories, not random decoration: cyan for runtime, violet for release, green for health, pink for creative or community signals.
- Avoid red unless something truly needs attention.
- Pair neon badges with a strong title, hero image, or animated header; otherwise they can look disconnected.
- Check contrast in both GitHub light and dark themes.

## Best For

- AI agents, automation, and tooling.
- Creative coding and interactive demos.
- Portfolio repositories.
- Games, visualizers, and experiments.
- Developer products with a distinctive brand voice.
