# Security Policy

`readme-ux-kit` is primarily a documentation and SVG asset repository. Security work here focuses on safe-to-embed Markdown and SVG content.

## Supported Scope

Security reports are in scope when they involve:

- unsafe SVG content, such as scripts or external references
- malicious links in Markdown examples
- generated preview output that could mislead users into copying unsafe snippets
- dependency or release workflow issues that affect this repository

Out of scope:

- general design preferences
- broken visual rendering without a security impact
- reports about third-party services linked from example placeholders

## Reporting a Concern

Please do not open a public issue for a security concern.

Report privately by contacting the repository maintainer through GitHub. Include:

- affected file path
- a short description of the risk
- reproduction steps, if applicable
- suggested fix, if known

## SVG Safety Rules

SVG assets in this repository should:

- parse as valid XML
- include a `viewBox`
- avoid `<script>`
- avoid external `href` and `src` references
- keep animation self-contained

Run the local SVG validation check before submitting asset changes:

```bash
npm run check:svg
```

## Preview Safety

Generated previews should be regenerated and checked after asset changes:

```bash
npm run generate:previews
npm run check:previews
```

Generated preview files under `previews/assets/` should not be hand-edited.
