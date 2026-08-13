# FAQ

> Maturity: `stable`

FAQ sections reduce friction near the end of a README. They answer objections, clarify scope, explain compatibility, and route readers to the right next step without interrupting the main flow.

Use FAQs for project boundaries, support policy, installation issues, licensing, roadmap expectations, and operational concerns.

## Compact FAQ

```markdown
## FAQ

<details>
  <summary><strong>Who is this project for?</strong></summary>

  It is for maintainers who want a polished README, reusable visual components, and GitHub-compatible snippets without building a full documentation site.
</details>

<details>
  <summary><strong>Can I use the assets in another repository?</strong></summary>

  Yes. Copy the assets into your project or reference public raw GitHub URLs when the source repository is public.
</details>

<details>
  <summary><strong>Does this require JavaScript?</strong></summary>

  No. The snippets use Markdown, safe HTML, SVG assets, and GitHub-supported rendering behavior.
</details>
```

## Product FAQ

```markdown
## FAQ

| Question | Answer |
| --- | --- |
| What problem does this solve? | It gives maintainers ready-made README sections that look polished and remain easy to maintain. |
| Is it framework-specific? | No. Most components are plain Markdown or HTML and can be copied into any GitHub README. |
| Can I customize the visuals? | Yes. Replace raw asset URLs, edit SVG files, or generate custom typing headers. |
| Is it suitable for private repos? | Yes. Use relative paths for assets stored inside the same private repository. |
```

## Support FAQ

```markdown
## Support

<details>
  <summary><strong>How do I report a bug?</strong></summary>

  Open an issue with:

  - The component or template name.
  - A screenshot or rendered README link.
  - The expected behavior.
  - The actual behavior.
</details>

<details>
  <summary><strong>How are releases handled?</strong></summary>

  Releases are versioned through the repository release workflow. Check the changelog and GitHub releases before upgrading copied snippets.
</details>

<details>
  <summary><strong>What is the compatibility target?</strong></summary>

  Components are designed for GitHub Markdown first. Other Markdown renderers may support a different subset of HTML and SVG behavior.
</details>
```

## Technical FAQ

```markdown
## Technical FAQ

<details>
  <summary><strong>Why are some examples written in HTML?</strong></summary>

  GitHub Markdown allows a safe subset of HTML. It is useful for centered images, tables, alignment, collapsible sections, and badge rows.
</details>

<details>
  <summary><strong>Why not use custom CSS?</strong></summary>

  GitHub strips most custom styles from rendered Markdown. These components rely on structures that survive GitHub sanitization.
</details>

<details>
  <summary><strong>How should I handle broken raw image links?</strong></summary>

  Prefer relative paths when the asset lives in the same repository. Use raw GitHub URLs only for public, stable assets.
</details>
```

## FAQ With Visual Divider

```markdown
<p align="center">
  <img alt="FAQ divider" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/dividers/static/divider_dot_center.svg">
</p>

## FAQ

<details>
  <summary><strong>Can I copy only one component?</strong></summary>

  Yes. Each component is designed to work independently.
</details>
```

## Question Bank

```text
Project fit:
- Who is this project for?
- What is intentionally out of scope?
- When should I choose a different tool?

Setup:
- What versions are supported?
- Does it work on Windows, macOS, and Linux?
- How do I configure environment variables?

Operations:
- How are releases handled?
- What is the support policy?
- Where do I report security issues?

Assets:
- Can I use raw GitHub URLs?
- Can I edit the SVG files?
- Do the animations work in private repositories?
```

## Design Rules

- Put FAQs near the end of the README, after core usage and examples.
- Answer real objections, not marketing questions.
- Keep each answer short. Link to deeper docs when needed.
- Use `<details>` for long answers and tables for short direct answers.
- Do not hide critical installation steps in the FAQ.

## Copy Checklist

- Remove questions that do not apply to the project.
- Keep the answer tone direct and specific.
- Include links for issues, security policy, releases, and docs where useful.
- Preview collapsed sections on GitHub.
