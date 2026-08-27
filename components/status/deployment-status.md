# Deployment Status

> Maturity: `stable`

Deployment status sections make operational health visible without turning a README into a full status page. Use them for services, APIs, CLIs with hosted infrastructure, demos, dashboards, and internal platforms.

Place deployment status near the top for live products, or after quick start for libraries that also ship a hosted example.

## Production Status Panel

```markdown
## Deployment Status

| Environment | Status | Version | Region | Last deploy |
| --- | --- | --- | --- | --- |
| Production | ![Live](https://img.shields.io/badge/live-16a34a?style=flat-square) | `v1.8.0` | `us-east-1` | `2026-05-02` |
| Staging | ![Ready](https://img.shields.io/badge/ready-2563eb?style=flat-square) | `v1.9.0-rc.1` | `us-east-1` | `2026-05-01` |
| Preview | ![Ephemeral](https://img.shields.io/badge/ephemeral-7c3aed?style=flat-square) | per branch | dynamic | on pull request |
```

## Live Service Row

```markdown
[![Production](https://img.shields.io/badge/production-live-16a34a?style=for-the-badge)](https://status.example.com)
[![API](https://img.shields.io/badge/api-healthy-0f766e?style=for-the-badge)](https://api.example.com/health)
[![Deploy](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/deploy.yml?branch=main&style=for-the-badge&label=deploy&color=2563eb)](https://github.com/OWNER/REPO/actions)
[![Uptime](https://img.shields.io/badge/uptime-99.95%25-16a34a?style=for-the-badge)](https://status.example.com)
```

## Operational Dashboard Header

```markdown
<p align="center">
  <img alt="Status dashboard header" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_status_dashboard.svg">
</p>

## Operations

| Signal | Target | Current |
| --- | ---: | ---: |
| Availability | `99.9%` | `99.95%` |
| API latency | `< 300ms p95` | `218ms p95` |
| Error rate | `< 0.1%` | `0.03%` |
| Queue delay | `< 60s` | `12s` |
```

## Release Promotion Flow

```markdown
## Deployment Flow

| Stage | Gate | Command |
| --- | --- | --- |
| Build | Typecheck, lint, test | `npm run build` |
| Staging | Smoke test and migration dry run | `npm run deploy:staging` |
| Production | Manual approval and release tag | `npm run deploy:production` |
| Verify | Health checks and synthetic request | `npm run smoke:production` |
```

## Incident Banner

Use this only when a live user-facing issue exists.

```markdown
> [!WARNING]
> Production is currently degraded. Follow updates at <https://status.example.com>.
```

## Maintenance Banner

```markdown
> [!NOTE]
> Scheduled maintenance: `2026-05-05 02:00-03:00 UTC`. API writes may be temporarily delayed.
```

## Health Check Block

````markdown
## Health Checks

```bash
curl https://api.example.com/health/ready
```

```json
{
  "status": "ok",
  "database": "connected",
  "queue": "ready",
  "version": "1.8.0"
}
```
````

## Status Icons

```markdown
| Status | Icon | Meaning |
| --- | --- | --- |
| Live | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_live.svg" width="20" alt="Live"> | Serving production traffic |
| Success | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_success.svg" width="20" alt="Success"> | Passing expected checks |
| Warning | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_warning.svg" width="20" alt="Warning"> | Needs attention |
| Danger | <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/icons/status/icon_danger.svg" width="20" alt="Danger"> | User-facing issue or broken state |
```

## Design Rules

- Distinguish build status from deployment status. A passing build does not prove production is healthy.
- Link badges to verifiable systems: status page, workflow run, health endpoint, or release page.
- Use exact dates for deployments and maintenance windows.
- Keep incident banners temporary and remove them after resolution.
- Avoid claiming uptime or SLOs unless the numbers are maintained.

## Copy Checklist

- Replace `OWNER`, `REPO`, workflow names, URLs, regions, and versions.
- Confirm health endpoints are safe to expose publicly.
- Keep production, staging, and preview status visually distinct.
- Update deployment dates whenever examples become real project docs.
