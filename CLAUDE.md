# CLAUDE.md — Project Context & Verification Rules

Read [`AGENTS.md`](AGENTS.md) and [`.codex/designer-session.md`](.codex/designer-session.md) before modifying SVG assets, documentation, or Python/JavaScript modules.

## Key Verification Gate

- Always run `npm run quality:gate` (which runs `npm run check:all`) and `git diff --check` before completing any task.
- Never commit or push unless explicitly instructed by the user.
- Keep all Markdown table lines under 180 characters so `npm run check:markdown` passes with zero warnings.
