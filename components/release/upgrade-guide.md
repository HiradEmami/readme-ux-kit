# Upgrade Guide

> Maturity: `stable`
> Best for: Migration steps and verification checks.
> Compatible themes: `minimal`, `docs-clean`, `enterprise`, `terminal`, `open-source-classic`
> Compatible templates: `minimal`, `open-source-lib`, `backend-service`, `cli-tool`, `sdk-reference`

## Purpose

Use this component when a README needs migration steps and verification checks.

## Copy-Ready Markdown

```markdown
## Upgrade Guide

| Version | Change | Action |
| --- | --- | --- |
| `VERSION` | `CHANGE_SUMMARY` | `USER_ACTION` |

Run `VERIFY_COMMAND` after upgrading.
```

## Required Placeholders

- `OLD_VERSION`
- `NEW_VERSION`

## Optional Placeholders

- `DOCS_URL`
- `ISSUES_URL`
- `SUPPORT_URL`

## Design Rules

- Keep this block short enough to scan in one pass.
- Prefer factual wording over claims that need proof.
- Link to source material when the block references policy, releases, docs, or support.
- Remove rows that do not apply instead of leaving filler.

## GitHub Compatibility Notes

- Uses standard GitHub Markdown tables, lists, links, and code spans.
- Does not require custom JavaScript, external CSS, or unsupported HTML.
- Keep linked examples inside the target repository unless they are intentionally external.

## Do Not Use When

- The README already has a clearer, shorter version of the same information.
- The project cannot keep the listed links or statuses current.
- The section would create fake confidence around an unverified claim.

## Copy Checklist

- [ ] Replace every required placeholder.
- [ ] Remove irrelevant rows.
- [ ] Verify every link.
- [ ] Confirm the maturity marker fits the final README.
