# System Badges

> Maturity: `stable`

Clean, production-oriented badge rows for READMEs that need to communicate trust quickly: build health, release maturity, license, package status, platform support, security posture, and maintenance activity.

Use system badges near the top of a README, directly under the project title or hero section. Keep them factual, restrained, and easy to scan.

## Premium Row

```markdown
[![Release](https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=release&color=0f766e)](https://github.com/OWNER/REPO/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=for-the-badge&label=build&color=2563eb)](https://github.com/OWNER/REPO/actions)
[![Coverage](https://img.shields.io/codecov/c/github/OWNER/REPO?style=for-the-badge&label=coverage&color=16a34a)](https://codecov.io/gh/OWNER/REPO)
[![License](https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&label=license&color=475569)](../../LICENSE)
[![Security](https://img.shields.io/badge/security-reviewed-15803d?style=for-the-badge)](https://github.com/OWNER/REPO/security)
```

Preview:

[![Release](https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&label=release&color=0f766e)](https://github.com/OWNER/REPO/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=for-the-badge&label=build&color=2563eb)](https://github.com/OWNER/REPO/actions)
[![Coverage](https://img.shields.io/codecov/c/github/OWNER/REPO?style=for-the-badge&label=coverage&color=16a34a)](https://codecov.io/gh/OWNER/REPO)
[![License](https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&label=license&color=475569)](../../LICENSE)
[![Security](https://img.shields.io/badge/security-reviewed-15803d?style=for-the-badge)](https://github.com/OWNER/REPO/security)

Replace `OWNER`, `REPO`, `main`, and `ci.yml` with your repository details.

## Minimal System Row

For libraries and tools where the README should stay quiet and authoritative.

```markdown
[![npm](https://img.shields.io/npm/v/PACKAGE_NAME?style=flat-square&label=npm&color=cb3837)](https://www.npmjs.com/package/PACKAGE_NAME)
[![CI](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=flat-square&label=ci)](https://github.com/OWNER/REPO/actions)
[![TypeScript](https://img.shields.io/badge/types-TypeScript-3178c6?style=flat-square)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/github/license/OWNER/REPO?style=flat-square)](../../LICENSE)
```

## Backend Service Row

```markdown
[![API](https://img.shields.io/badge/api-stable-0f766e?style=for-the-badge)](https://github.com/OWNER/REPO/releases)
[![Docker](https://img.shields.io/docker/v/OWNER/IMAGE?style=for-the-badge&label=docker&color=2496ed)](https://hub.docker.com/r/OWNER/IMAGE)
[![Uptime](https://img.shields.io/badge/uptime-99.95%25-16a34a?style=for-the-badge)](https://status.example.com)
[![SLO](https://img.shields.io/badge/slo-250ms_p95-7c3aed?style=for-the-badge)](https://docs.example.com/slo)
[![OpenAPI](https://img.shields.io/badge/openapi-3.1-6ba539?style=for-the-badge)](https://spec.openapis.org/oas/latest.html)
```

## Machine Learning Row

```markdown
[![Model](https://img.shields.io/badge/model-production-0f766e?style=for-the-badge)](https://github.com/OWNER/REPO/releases)
[![Dataset](https://img.shields.io/badge/dataset-versioned-2563eb?style=for-the-badge)](./data)
[![Eval](https://img.shields.io/badge/eval-passing-16a34a?style=for-the-badge)](./reports)
[![Python](https://img.shields.io/badge/python-3.11+-3776ab?style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&color=475569)](../../LICENSE)
```

## Security And Compliance Row

```markdown
[![Security Policy](https://img.shields.io/badge/security-policy-15803d?style=flat-square)](../../SECURITY.md)
[![SBOM](https://img.shields.io/badge/sbom-available-2563eb?style=flat-square)](./sbom.json)
[![Signed Releases](https://img.shields.io/badge/releases-signed-7c3aed?style=flat-square)](https://github.com/OWNER/REPO/releases)
[![Dependencies](https://img.shields.io/librariesio/github/OWNER/REPO?style=flat-square&label=dependencies)](https://libraries.io/github/OWNER/REPO)
```

## Design Rules

- Lead with the most decision-critical signal: release, build, package, or deployment.
- Limit the first row to four to six badges. Move secondary metrics deeper into the README.
- Prefer consistent badge styles inside a row: `for-the-badge`, `flat-square`, or `plastic`, not a mix.
- Use reserved color meaning: green for healthy, blue for platform or process, slate for neutral metadata, red only for warnings or failing states.
- Link every badge to the page where a reader can verify the claim.

## Copy Checklist

- Replace all placeholder values: `OWNER`, `REPO`, `PACKAGE_NAME`, `IMAGE`, and custom links.
- Confirm workflow filenames match your repository, such as `ci.yml`, `test.yml`, or `release.yml`.
- Keep alt text descriptive: `Build`, `Coverage`, `License`, not `badge`.
- Avoid vanity-only counts in the first row unless community traction is central to the project.
