# Terminal Blocks

> Maturity: `stable`

README terminal blocks should feel precise, runnable, and calm. Use them for installation, quick starts, deployment commands, CLI walkthroughs, expected output, and troubleshooting.

Prefer real commands over decorative terminal screenshots. Text blocks are searchable, copyable, accessible, and easier to maintain.

## Quick Start Terminal

````markdown
```bash
git clone https://github.com/OWNER/REPO.git
cd REPO
npm install
npm run dev
```
````

## Command Plus Output

Use separate blocks when the command and output both matter.

````markdown
```bash
npm run health
```

```text
service: api
status: ok
database: connected
queue: ready
```
````

## Premium CLI Walkthrough

````markdown
### Create a project

```bash
npx PACKAGE_NAME init my-app
cd my-app
```

### Start locally

```bash
npm run dev
```

### Ship a production build

```bash
npm run build
npm run start
```
````

## Terminal Card With HTML

Use this when you want a framed command block without relying on custom CSS.

````html
<table>
  <tr>
    <td><strong>Local development</strong></td>
  </tr>
  <tr>
    <td>

```bash
npm install
npm run dev
```

  </td>
  </tr>
</table>
````

GitHub can render fenced code inside HTML tables, but spacing is sensitive. Keep blank lines around the code fence.

## Multi-Environment Commands

```markdown
| Environment | Command |
| --- | --- |
| Local | `npm run dev` |
| Test | `npm run test` |
| Production build | `npm run build` |
| Production start | `npm run start` |
```

## Deployment Terminal

````markdown
```bash
docker build -t OWNER/IMAGE:latest .
docker run --env-file .env -p 3000:3000 OWNER/IMAGE:latest
```

```text
server listening on http://localhost:3000
health check passed
```
````

## Troubleshooting Terminal

````markdown
<details>
  <summary><strong>Port already in use</strong></summary>

  Find the process using the port:

  ```bash
  lsof -i :3000
  ```

  Start the app on a different port:

  ```bash
  PORT=3001 npm run dev
  ```
</details>
````

## Polished Prompt Style

Use prompts only when they improve readability. Avoid including prompts in commands readers need to copy.

````markdown
```text
$ npm run dev
> app@1.0.0 dev
> vite

Local: http://localhost:5173
```
````

For copyable commands, omit `$`:

````markdown
```bash
npm run dev
```
````

## Visual Terminal Header

```markdown
<p align="center">
  <img alt="Terminal header" src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/headers/static/header_terminal_typing.svg">
</p>
```

## Design Rules

- Use `bash`, `sh`, `powershell`, `json`, `text`, `ts`, or `py` fences so syntax highlighting is useful.
- Keep one intent per command block.
- Do not mix command prompts, comments, and output in a block meant to be copied.
- Show expected output only when it helps the reader verify success.
- Prefer environment variable names over real secrets: `$API_KEY`, not sample tokens.

## Copy Checklist

- Run or verify commands before publishing.
- Replace `OWNER`, `REPO`, `PACKAGE_NAME`, `IMAGE`, and ports.
- Keep OS-specific commands clearly labeled.
- Mark non-copyable transcripts as `text`.
