# Tabs

> Maturity: `draft`

GitHub Markdown does not support JavaScript-powered tabs, but you can create tab-like README patterns that are reliable, accessible, and easy to scan. Use these patterns for install methods, language examples, deployment targets, operating systems, and API variants.

Choose the pattern based on how much content each tab needs.

## Linkable Section Tabs

Best for substantial content. The navigation row links to normal headings, so each section remains readable and shareable.

````markdown
### Installation

[npm](#npm) | [pnpm](#pnpm) | [yarn](#yarn) | [Docker](#docker)

#### npm

```bash
npm install PACKAGE_NAME
```

#### pnpm

```bash
pnpm add PACKAGE_NAME
```

#### yarn

```bash
yarn add PACKAGE_NAME
```

#### Docker

```bash
docker pull OWNER/IMAGE:latest
```
````

## Table Tabs

Best when every option has a short command or small code sample.

```markdown
| Runtime | Command |
| --- | --- |
| npm | `npm install PACKAGE_NAME` |
| pnpm | `pnpm add PACKAGE_NAME` |
| yarn | `yarn add PACKAGE_NAME` |
| Docker | `docker pull OWNER/IMAGE:latest` |
```

## Details-Based Tabs

Best when you want the page to stay compact while allowing one option to expand at a time manually.

````markdown
<details open>
  <summary><strong>npm</strong></summary>

  ```bash
  npm install PACKAGE_NAME
  npm run dev
  ```
</details>

<details>
  <summary><strong>pnpm</strong></summary>

  ```bash
  pnpm add PACKAGE_NAME
  pnpm dev
  ```
</details>

<details>
  <summary><strong>Docker</strong></summary>

  ```bash
  docker compose up --build
  ```
</details>
````

Only one section should use `open` by default.

## Platform Matrix

```markdown
### Platform Support

| Platform | Status | Notes |
| --- | --- | --- |
| Linux | ![Supported](https://img.shields.io/badge/supported-yes-16a34a?style=flat-square) | Primary CI target |
| macOS | ![Supported](https://img.shields.io/badge/supported-yes-16a34a?style=flat-square) | Local development |
| Windows | ![Supported](https://img.shields.io/badge/supported-partial-f59e0b?style=flat-square) | WSL recommended |
```

## API Variant Tabs

````markdown
### Usage

[TypeScript](#typescript) | [Python](#python) | [cURL](#curl)

#### TypeScript

```ts
import { client } from "PACKAGE_NAME";

const result = await client.run({
  input: "Summarize this repository",
});
```

#### Python

```py
from package_name import Client

client = Client()
result = client.run(input="Summarize this repository")
```

#### cURL

```bash
curl -X POST https://api.example.com/run \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input":"Summarize this repository"}'
```
````

## Visual Tab Divider

Use a divider when tab-like sections are visually dense.

```markdown
<p align="center">
  <img alt="Section divider" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/dividers/static/divider_minimal_clean.svg">
</p>
```

## Design Rules

- Use linkable headings for long content and tables for short comparisons.
- Keep tab labels parallel: `npm`, `pnpm`, `Docker`, not `Install with npm`, `pnpm`, `container`.
- Do not simulate tabs with images only; the content should remain selectable and searchable.
- Keep examples equivalent across tabs so readers can compare quickly.
- Use GitHub heading anchors for deep links, but verify generated anchors if headings contain punctuation.

## Copy Checklist

- Replace package, image, endpoint, and repository placeholders.
- Keep one default option first, usually the most common path.
- Make every code sample runnable for that option.
- Preview anchor links after GitHub renders the README.
