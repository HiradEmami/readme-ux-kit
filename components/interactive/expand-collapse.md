# Expand And Collapse

> Maturity: `stable`

GitHub-compatible disclosure sections for READMEs that need depth without overwhelming the first scan. Use them for advanced setup, troubleshooting, API details, benchmark notes, architecture diagrams, migration notes, and long examples.

The core primitive is native HTML: `<details>` with a `<summary>`. It works in GitHub Markdown without JavaScript.

## Premium Disclosure

````markdown
<details>
  <summary><strong>Production deployment checklist</strong></summary>

  ### Required checks

  - Confirm `DATABASE_URL`, `REDIS_URL`, and `APP_SECRET` are set in the target environment.
  - Run the migration plan against a staging snapshot.
  - Verify health checks return `200` from `/health/live` and `/health/ready`.
  - Review the rollback command before promoting the release.

  ```bash
  npm run build
  npm run db:migrate
  npm run smoke:test
  ```
</details>
````

Use a blank line after `<summary>` and before `</details>` so nested Markdown renders correctly.

## Compact FAQ

```markdown
<details>
  <summary><strong>Does this work with private repositories?</strong></summary>

Yes. Use relative paths for local assets and avoid raw GitHub URLs that require public access.
</details>

<details>
  <summary><strong>Can I use this in GitHub issues?</strong></summary>

Yes. GitHub issues, pull requests, discussions, and READMEs all support `<details>` blocks.
</details>

<details>
  <summary><strong>Should every section be collapsible?</strong></summary>

No. Keep core installation, quick start, and usage visible. Collapse supporting detail.
</details>
```

## Technical Deep Dive

```markdown
<details>
  <summary><strong>Architecture notes</strong></summary>

  The service is split into three operational layers:

  | Layer | Responsibility | Runtime |
  | --- | --- | --- |
  | API | Request validation and routing | Node.js |
  | Worker | Async jobs and retries | BullMQ |
  | Store | Durable state and audit records | PostgreSQL |

  <p align="center">
    <img alt="Architecture divider" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/dividers/animated/lines/divider_data_flow.svg">
  </p>

  The API remains stateless. Workers own retry policy, backoff, and dead-letter handling.
</details>
```

## Troubleshooting Drawer

````markdown
<details>
  <summary><strong>Build fails with missing environment variables</strong></summary>

  Create a local `.env` file from the template:

  ```bash
  cp .env.example .env
  ```

  Then fill the required values:

  ```text
  DATABASE_URL=
  REDIS_URL=
  APP_SECRET=
  ```

  Run the validation command before starting the app:

  ```bash
  npm run env:check
  ```
</details>
````

## Nested Disclosure

Use nesting only when the content is genuinely layered. Two levels is usually enough.

```markdown
<details>
  <summary><strong>Advanced configuration</strong></summary>

  <details>
    <summary>Cache settings</summary>

    - `CACHE_TTL_SECONDS` controls default cache lifetime.
    - `CACHE_NAMESPACE` isolates environments that share Redis.
  </details>

  <details>
    <summary>Queue settings</summary>

    - `QUEUE_CONCURRENCY` controls parallel job processing.
    - `QUEUE_RETRY_LIMIT` controls retry attempts before dead-lettering.
  </details>
</details>
```

## Design Rules

- Keep the summary short, specific, and action-oriented.
- Do not hide primary setup instructions, project purpose, or the main usage example.
- Put one topic per disclosure. If the content needs multiple headings, consider a normal section.
- Avoid collapsed sections inside tables; rendering is fragile across Markdown surfaces.
- Use bold text inside `<summary>` for stronger scanability.

## Accessibility Notes

- The native `<details>` element is keyboard-accessible in modern browsers.
- Write summaries as labels, not teasers. A reader should know exactly what opens.
- Do not use animated assets as the only signal that content is expandable.
- Keep decorative images inside expanded content and give them useful `alt` text.

## Copy Checklist

- Add a blank line after each `<summary>`.
- Keep fenced code blocks indented consistently inside the disclosure.
- Preview the README on GitHub before publishing.
- Collapse supporting detail, not the value proposition.
