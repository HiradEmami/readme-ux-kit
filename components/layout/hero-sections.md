# Hero Sections

> Maturity: `draft`

Hero sections establish what the project is, why it matters, and where a reader should go next. In a README, the best hero is compact: one strong visual, one clear positioning line, key links, and a fast path to installation or usage.

Use heroes for public libraries, developer tools, research projects, AI systems, portfolios, and productized open-source repositories.

## Product Hero

```markdown
<p align="center">
  <img alt="Project banner" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/banners/energy/banner_gradient_cyber_line_sweep.svg">
</p>

<h1 align="center">PROJECT_NAME</h1>

<p align="center">
  A concise, high-signal sentence that explains the project outcome, audience, and value.
</p>

<p align="center">
  <a href="https://github.com/OWNER/REPO/releases">
    <img alt="Release" src="https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=release&color=2563eb">
  </a>
  <a href="https://github.com/OWNER/REPO/actions">
    <img alt="Build" src="https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=for-the-badge&label=build&color=16a34a">
  </a>
  <a href="../../LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&color=475569">
  </a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> |
  <a href="#features">Features</a> |
  <a href="#documentation">Documentation</a> |
  <a href="#roadmap">Roadmap</a>
</p>
```

## Developer Tool Hero

````markdown
<p align="center">
  <img alt="Terminal-style header" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_terminal_typing.svg">
</p>

<h1 align="center">PACKAGE_NAME</h1>

<p align="center">
  Build, validate, and ship production-ready workflows from a single command.
</p>

```bash
npx PACKAGE_NAME init my-app
cd my-app
npm run dev
```

<p align="center">
  <a href="#installation">Installation</a> |
  <a href="#usage">Usage</a> |
  <a href="#configuration">Configuration</a>
</p>
````

## AI Project Hero

```markdown
<p align="center">
  <img alt="AI system visual" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/visuals/neural_singularity_reactor.svg" width="720">
</p>

<h1 align="center">PROJECT_NAME</h1>

<p align="center">
  Reproducible evaluations, transparent model behavior, and deployment-ready inference workflows.
</p>

<p align="center">
  <img alt="Model" src="https://img.shields.io/badge/model-production-0f766e?style=for-the-badge">
  <img alt="Eval" src="https://img.shields.io/badge/eval-passing-16a34a?style=for-the-badge">
  <img alt="Dataset" src="https://img.shields.io/badge/dataset-versioned-2563eb?style=for-the-badge">
</p>
```

## Minimal Library Hero

````markdown
# PACKAGE_NAME

> A small, reliable library for doing one important thing well.

[![npm](https://img.shields.io/npm/v/PACKAGE_NAME?style=flat-square&label=npm&color=cb3837)](https://www.npmjs.com/package/PACKAGE_NAME)
[![CI](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=flat-square&label=ci)](https://github.com/OWNER/REPO/actions)
[![License](https://img.shields.io/github/license/OWNER/REPO?style=flat-square)](../../LICENSE)

```bash
npm install PACKAGE_NAME
```
````

## Hero With Visual Divider

```markdown
<p align="center">
  <img alt="Project banner" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/banners/minimal/banner_soft_glow.svg">
</p>

<h1 align="center">PROJECT_NAME</h1>

<p align="center">
  A focused toolkit for building polished README experiences.
</p>

<p align="center">
  <img alt="Divider" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/dividers/static/divider_minimal_clean.svg">
</p>
```

## Copy Variants

```text
Open-source library: "A small, typed toolkit for building reliable developer workflows."
Backend service:     "A production-ready service template with observability, jobs, and clean deploys."
AI project:          "A reproducible evaluation system for comparing prompts, models, and datasets."
Research project:    "A transparent implementation with experiments, results, and replication notes."
Portfolio project:   "A polished product case study with architecture, workflow, and delivery details."
```

## Design Rules

- Keep the hero above the fold short. Readers should reach installation or usage quickly.
- Use one primary visual, not a stack of unrelated banners.
- Put badges below the value statement, not before the reader knows what the project does.
- Use centered HTML sparingly. It works best for the hero, not every README section.
- Keep navigation links to four or five destinations.

## Copy Checklist

- Replace `PROJECT_NAME`, `OWNER`, `REPO`, `PACKAGE_NAME`, and workflow names.
- Verify every raw asset URL exists.
- Keep the first sentence concrete and outcome-focused.
- Preview in GitHub light and dark themes.
