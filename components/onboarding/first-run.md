# First Run

> Maturity: `stable`
> Best for: First successful command path with expected output.
> Compatible themes: `minimal`, `docs-clean`, `enterprise`, `terminal`, `open-source-classic`
> Compatible templates: `minimal`, `open-source-lib`, `backend-service`, `cli-tool`, `sdk-reference`

## Purpose

Use this component when a README needs first successful command path with expected output.

## Copy-Ready Markdown

```markdown
## First Run

1. Confirm prerequisites for `PROJECT_NAME`.
2. Run `INSTALL_COMMAND`.
3. Run `RUN_COMMAND`.
4. Compare the output with `EXPECTED_OUTPUT`.
5. Open `DOCS_URL` if the first run fails.
```

## Required Placeholders

- `RUN_COMMAND`

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
