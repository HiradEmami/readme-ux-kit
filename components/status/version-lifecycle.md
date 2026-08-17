# Version Lifecycle

> Maturity: `stable`

Version lifecycle sections explain what is stable, what is changing, and what users should do next. They are especially useful for libraries, APIs, CLIs, templates, datasets, and services with multiple supported versions.

Use this section near installation for libraries and near release notes for apps or services.

## Support Matrix

```markdown
## Version Support

| Version | Status | Supported until | Notes |
| --- | --- | --- | --- |
| `v2.x` | ![Current](https://img.shields.io/badge/current-16a34a?style=flat-square) | active | Recommended for new projects |
| `v1.x` | ![Maintenance](https://img.shields.io/badge/maintenance-f59e0b?style=flat-square) | `2026-12-31` | Security fixes only |
| `v0.x` | ![Deprecated](https://img.shields.io/badge/deprecated-ef4444?style=flat-square) | ended | Upgrade required |
```

## Lifecycle Badge Row

```markdown
[![Release](https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=release&color=2563eb)](https://github.com/OWNER/REPO/releases)
[![Lifecycle](https://img.shields.io/badge/lifecycle-stable-16a34a?style=for-the-badge)](#version-support)
[![Maintenance](https://img.shields.io/badge/maintenance-active-0f766e?style=for-the-badge)](#support-policy)
[![API](https://img.shields.io/badge/api-v2-7c3aed?style=for-the-badge)](#migration-guide)
```

## Release Channels

```markdown
## Release Channels

| Channel | Install | Stability | Audience |
| --- | --- | --- | --- |
| Stable | `npm install PACKAGE_NAME` | Production-ready | Most users |
| Next | `npm install PACKAGE_NAME@next` | Release candidate | Early adopters |
| Canary | `npm install PACKAGE_NAME@canary` | Experimental | Maintainers and testers |
```

## Migration Notice

```markdown
> [!IMPORTANT]
> `v1.x` enters maintenance on `2026-06-01` and reaches end of support on `2026-12-31`.
> New projects should use `v2.x`. Existing projects should follow the migration guide before upgrading.
```

## Migration Checklist

````markdown
## Upgrade From v1 To v2

1. Update the package.

```bash
npm install PACKAGE_NAME@latest
```

2. Replace deprecated options.

```diff
- createClient({ token: API_TOKEN })
+ createClient({ apiKey: API_TOKEN })
```

3. Run the compatibility check.

```bash
npm run check:upgrade
```
````

## API Stability Table

```markdown
## API Stability

| Surface | Status | Compatibility promise |
| --- | --- | --- |
| Public package exports | Stable | Semver-protected |
| CLI commands | Stable | Breaking changes only in major releases |
| Config file format | Evolving | Migration notes provided |
| Internal modules | Private | No compatibility guarantee |
```

## Lifecycle Icons

```markdown
| Status | Icon | Meaning |
| --- | --- | --- |
| Current | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_success.svg" width="20" alt="Current"> | Recommended release line |
| Maintenance | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_notice.svg" width="20" alt="Maintenance"> | Fixes only |
| Deprecated | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_deprecated.svg" width="20" alt="Deprecated"> | Upgrade required |
| Unsupported | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_x_circle.svg" width="20" alt="Unsupported"> | No fixes planned |
```

## Release Progress

```markdown
<p align="center">
  <img alt="Release progress" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/progress_bars/progress_bar_segment.svg">
</p>

| Milestone | Status |
| --- | --- |
| API freeze | Complete |
| Migration guide | Complete |
| Release candidate | In progress |
| Stable release | Planned |
```

## Design Rules

- Use exact dates for deprecation and end-of-support windows.
- State what "maintenance" means: security only, bug fixes, or no new features.
- Keep semver promises clear and narrow.
- Separate public API from internal modules.
- Link migrations to concrete examples, not only prose.

## Copy Checklist

- Replace package names, versions, dates, and install commands.
- Keep support windows current.
- Link releases, changelog, and migration guide.
- Mark unsupported versions plainly.
