from pathlib import Path
import argparse
import json
import re
import tempfile

from src.modules.common.repo import (
    HEADING_RE,
    rel_path,
    repo_root,
    slugify_heading,
    strip_fenced_blocks,
    write_json,
)


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/markdown/markdown_quality.py"
DEFAULT_MARKDOWN_ROOTS = (
    "README.md",
    "NAVIGATION.md",
    "CONTRIBUTING.md",
    "docs",
    "components",
    "templates",
    "themes",
    "previews/assets",
)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
DETAILS_OPEN_RE = re.compile(r"^\s*<details\b", re.IGNORECASE | re.MULTILINE)
DETAILS_CLOSE_RE = re.compile(r"^\s*</details>", re.IGNORECASE | re.MULTILINE)


def issue(code, path, message, severity="error", line=None):
    return {
        "code": code,
        "path": Path(path).as_posix() if path else "",
        "message": message,
        "severity": severity,
        "line": line,
    }


def markdown_files(root, include_dirs=DEFAULT_MARKDOWN_ROOTS):
    root = Path(root)
    files = []
    for item in include_dirs:
        target = root / item
        if target.is_file() and target.suffix.lower() == ".md":
            files.append(target)
        elif target.exists():
            files.extend(target.rglob("*.md"))
    return sorted(set(files), key=lambda path: path.as_posix().lower())


def fence_issues(root):
    issues = []
    for path in markdown_files(root):
        active = None
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = FENCE_RE.match(line)
            if not match:
                continue
            marker = match.group(1)
            fence = (marker[0], len(marker))
            if active is None:
                active = (fence, number)
            elif fence[0] == active[0][0] and fence[1] >= active[0][1]:
                active = None
        if active is not None:
            issues.append(issue("unclosed-code-fence", rel_path(path, root), "Code fence is not closed.", line=active[1]))
    return issues


def duplicate_anchor_issues(root):
    issues = []
    for path in markdown_files(root):
        relative = rel_path(path, root)
        if relative.startswith("previews/assets/"):
            continue
        text = strip_fenced_blocks(path.read_text(encoding="utf-8"))
        seen = {}
        for number, line in enumerate(text.splitlines(), start=1):
            match = HEADING_RE.match(line)
            if not match:
                continue
            anchor = slugify_heading(match.group(2))
            if not anchor:
                continue
            if anchor in seen:
                issues.append(
                    issue(
                        "duplicate-heading-anchor",
                        relative,
                        f"Heading produces duplicate anchor #{anchor}; first seen on line {seen[anchor]}.",
                        severity="warning",
                        line=number,
                    )
                )
            else:
                seen[anchor] = number
    return issues


def details_balance_issues(root):
    issues = []
    for path in markdown_files(root):
        text = strip_fenced_blocks(path.read_text(encoding="utf-8"))
        opens = len(DETAILS_OPEN_RE.findall(text))
        closes = len(DETAILS_CLOSE_RE.findall(text))
        if opens != closes:
            issues.append(issue("unbalanced-details", rel_path(path, root), f"Found {opens} <details> and {closes} </details> tags."))
    return issues


def wide_table_issues(root, limit=220):
    issues = []
    for path in markdown_files(root):
        relative = rel_path(path, root)
        if relative.startswith("previews/assets/"):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|") and len(line) > limit:
                issues.append(
                    issue(
                        "wide-markdown-table",
                        relative,
                        f"Table row is {len(line)} characters; consider shortening for repository browsing.",
                        severity="warning",
                        line=number,
                    )
                )
    return issues


def readme_composition_issues(root):
    path = Path(root) / "README.md"
    if not path.exists():
        return [issue("missing-root-readme", "README.md", "Root README.md is required.")]
    text = path.read_text(encoding="utf-8")
    required = ["## Start Here", "Browse assets", "Pick a template", "Pick a theme", "Copy components"]
    return [
        issue("missing-readme-start-here", "README.md", f"README.md should include {value}.")
        for value in required
        if value not in text
    ]


def collect_markdown_issues(root=None):
    root = Path(root or repo_root()).resolve()
    checks = [fence_issues, duplicate_anchor_issues, details_balance_issues, wide_table_issues, readme_composition_issues]
    issues = []
    for check in checks:
        issues.extend(check(root))
    return sorted(issues, key=lambda item: (item["severity"], item["path"], item["line"] or 0, item["code"]))


def snippet_payload():
    snippets = [
        {
            "id": "asset-markdown-link",
            "label": "Asset Markdown Link",
            "description": "Clickable image syntax for SVG assets in README files.",
            "language": "markdown",
            "snippet": "[![ASSET_LABEL](RAW_ASSET_URL)](TARGET_URL)",
        },
        {
            "id": "asset-html-image",
            "label": "Asset HTML Image",
            "description": "HTML image syntax for width control and aligned README layouts.",
            "language": "html",
            "snippet": '<p align="center"><img alt="ASSET_LABEL" src="RAW_ASSET_URL" width="100%"></p>',
        },
        {
            "id": "details-markdown-copy",
            "label": "Collapsible Markdown Copy Block",
            "description": "Preview-page section for copyable Markdown usage.",
            "language": "markdown",
            "snippet": "<details>\n<summary>Markdown</summary>\n\n```markdown\nCONTENT\n```\n</details>",
        },
        {
            "id": "details-html-copy",
            "label": "Collapsible HTML Copy Block",
            "description": "Preview-page section for copyable HTML usage.",
            "language": "markdown",
            "snippet": "<details>\n<summary>HTML</summary>\n\n```html\nCONTENT\n```\n</details>",
        },
        {
            "id": "badge-row",
            "label": "Centered Badge Row",
            "description": "Compact badge group for root README headers.",
            "language": "html",
            "snippet": '<p align="center">\n  <a href="URL"><img alt="LABEL" src="BADGE_URL"></a>\n</p>',
        },
        {
            "id": "feature-table",
            "label": "Feature Table",
            "description": "Readable table for features, use cases, and project capability summaries.",
            "language": "markdown",
            "snippet": "| Feature | Description |\n| --- | --- |\n| FEATURE_NAME | FEATURE_VALUE |",
        },
        {
            "id": "status-table",
            "label": "Status Table",
            "description": "Operational status table for services, datasets, releases, and docs.",
            "language": "markdown",
            "snippet": "| Signal | Status | Notes |\n| --- | --- | --- |\n| SIGNAL_NAME | STATUS_VALUE | NOTES |",
        },
        {
            "id": "theme-asset-callout",
            "label": "Theme Asset Callout",
            "description": "Small pairing block for theme docs and recipes.",
            "language": "markdown",
            "snippet": "> Theme pair: `THEME_NAME` with `ASSET_NAME` for SECTION_NAME.",
        },
    ]
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "snippetCount": len(snippets),
        "snippets": snippets,
    }


def write_snippets(output):
    payload = snippet_payload()
    return write_json(output, payload), payload["snippetCount"]


def check_snippets(output):
    output = Path(output)
    expected = json.dumps(snippet_payload(), indent=2, sort_keys=True) + "\n"
    if not output.exists():
        return "missing"
    if output.read_text(encoding="utf-8") != expected:
        return "changed"
    return None


def print_issues(issues):
    if not issues:
        print("Markdown quality checks passed.")
        return
    has_errors = any(item["severity"] == "error" for item in issues)
    print("Markdown quality checks failed:" if has_errors else "Markdown quality checks passed with warnings:")
    for item in issues[:80]:
        line = f":{item['line']}" if item.get("line") else ""
        print(f"- [{item['severity']}] {item['path']}{line}: {item['code']} - {item['message']}")
        annotation = "error" if item["severity"] == "error" else "warning"
        print(f"::{annotation} file={item['path']},line={item.get('line') or 1}::{item['code']}: {item['message']}")
    if len(issues) > 80:
        print(f"... and {len(issues) - 80} more")


def run_self_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "docs").mkdir()
        (root / "README.md").write_text(
            "# Demo\n\n## Start Here\n\nBrowse assets\nPick a template\nPick a theme\nCopy components\n",
            encoding="utf-8",
        )
        (root / "docs" / "ok.md").write_text("# One\n\n```bash\nnpm test\n```\n", encoding="utf-8")
        assert fence_issues(root) == []
        (root / "docs" / "bad.md").write_text("# One\n\n```bash\nnpm test\n", encoding="utf-8")
        assert fence_issues(root)
        assert snippet_payload()["snippetCount"] >= 6
    print("markdown_quality.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Check Markdown quality and generate reusable Markdown snippets for the static site.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="site/data/markdown-snippets.json", help="Snippet JSON path relative to the repo root.")
    parser.add_argument("--check", action="store_true", help="Verify snippets and Markdown quality without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused Markdown self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    if args.check:
        status = check_snippets(output)
        issues = collect_markdown_issues(root)
        if status:
            print(f"::error file={rel_path(output, root)}::Markdown snippets are {status}. Run npm run generate:markdown-data.")
        print_issues(issues)
        has_errors = any(item["severity"] == "error" for item in issues)
        return 1 if status or has_errors else 0

    path, count = write_snippets(output)
    print(f"Wrote {count} Markdown snippet(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
