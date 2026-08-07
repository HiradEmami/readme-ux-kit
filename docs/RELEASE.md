# Release Process

Releases are manual and run through the `semantic-release` GitHub Actions workflow.

## Policy

- Releases are triggered from **Actions -> semantic-release -> Run workflow**.
- Releases must run from the `master` branch.
- The workflow uses the built-in `GITHUB_TOKEN`; no separate `GH_TOKEN` secret is required.
- The workflow runs `npm run check:all` before publishing, so stale previews, invalid SVGs, or broken generator syntax block the release.
- Use the `dry_run` workflow input to preview the next semantic-release result without publishing a GitHub release or updating `CHANGELOG.md`.

## Before Releasing

1. Confirm the working tree intended for release is merged into `master`.
2. Confirm generated previews are current with `npm run check:previews`.
3. Confirm all checks pass with `npm run check:all`.
4. Review `CHANGELOG.md` output after semantic-release opens the release commit.

## Commit Style

Semantic-release determines the next version from commit messages:

| Commit type | Release impact |
| --- | --- |
| `fix:` | Patch release |
| `feat:` | Minor release |
| `feat!:` or `BREAKING CHANGE:` | Major release |
| `docs:`, `chore:`, `refactor:`, `test:` | No release unless configured otherwise |

Use scopes to keep release notes readable, for example:

```text
feat(assets): add loading animations
fix(previews): correct stale generated output
docs(templates): improve backend service template guidance
```

For the full changelog policy, recommended scopes, and release-note review checklist, see [Changelog discipline](./CHANGELOG.md).
