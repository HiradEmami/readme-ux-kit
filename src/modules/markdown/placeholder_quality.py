from pathlib import Path
import argparse
import json
import re
import tempfile

from src.modules.common.repo import load_json, read_text, rel_path, repo_root, strip_fenced_blocks


DOCUMENTED_PLACEHOLDER_RE = re.compile(r"\|\s*`([A-Z][A-Z0-9_]*)`\s*\|")
ANGLE_PLACEHOLDER_RE = re.compile(r"<([a-z][a-z0-9 /_.-]{2,})>")
HTML_TAG_NAMES = {
    "a",
    "br",
    "code",
    "details",
    "div",
    "h1",
    "h2",
    "h3",
    "img",
    "p",
    "span",
    "strong",
    "summary",
    "table",
    "td",
    "th",
    "tr",
}


def issue(code, path, message, severity="error", line=None):
    return {
        "code": code,
        "path": Path(path).as_posix() if path else "",
        "message": message,
        "severity": severity,
        "line": line,
    }


def documented_placeholders(root):
    path = Path(root) / "docs" / "PLACEHOLDERS.md"
    if not path.exists():
        return set()
    return set(DOCUMENTED_PLACEHOLDER_RE.findall(read_text(path)))


def indexed_placeholders(root):
    root = Path(root)
    placeholders = set()
    index_files = [root / "components" / "index.json", root / "templates" / "index.json"]
    contract_files = sorted((root / "templates" / "contracts").glob("*.json"))
    for path in index_files + contract_files:
        if not path.exists():
            continue
        payload = load_json(path)
        collect_placeholders(payload, placeholders)
    return placeholders


def is_placeholder_field(key):
    if not isinstance(key, str):
        return False
    lowered = key.lower()
    return lowered.endswith("placeholders") or lowered.endswith("metadata") or lowered == "placeholderdefaults"


def collect_placeholders(value, output, placeholder_context=False):
    if isinstance(value, dict):
        for key, nested in value.items():
            next_context = placeholder_context or is_placeholder_field(key)
            if next_context and isinstance(key, str) and re.fullmatch(r"[A-Z][A-Z0-9_]*", key):
                output.add(key)
            collect_placeholders(nested, output, next_context)
    elif isinstance(value, list):
        for nested in value:
            collect_placeholders(nested, output, placeholder_context)
    elif placeholder_context and isinstance(value, str) and re.fullmatch(r"[A-Z][A-Z0-9_]*", value):
        output.add(value)


def indexed_maturity(root):
    root = Path(root)
    maturity = {}
    for index_path in [root / "components" / "index.json", root / "templates" / "index.json"]:
        if not index_path.exists():
            continue
        payload = load_json(index_path)
        for item in payload.get("components", []) + payload.get("templates", []):
            maturity[item.get("path", "")] = item.get("maturity", "")
    return maturity


def accidental_angle_placeholders(root):
    root = Path(root)
    issues = []
    maturity = indexed_maturity(root)
    for relative, value in maturity.items():
        if value != "stable":
            continue
        path = root / relative
        if not path.exists():
            continue
        text = strip_fenced_blocks(read_text(path))
        for number, line in enumerate(text.splitlines(), start=1):
            for match in ANGLE_PLACEHOLDER_RE.finditer(line):
                token = match.group(1).strip()
                first = token.split()[0].lower()
                if "=" in token or first in HTML_TAG_NAMES or token.startswith("/"):
                    continue
                issues.append(
                    issue(
                        "angle-placeholder-in-stable-file",
                        relative,
                        f"Stable Markdown should use uppercase snake-case placeholders instead of <{token}>.",
                        line=number,
                    )
                )
    return issues


def collect_placeholder_issues(root=None):
    root = Path(root or repo_root()).resolve()
    issues = []
    documented = documented_placeholders(root)
    if not documented:
        issues.append(issue("missing-placeholder-doc", "docs/PLACEHOLDERS.md", "Placeholder documentation is missing or empty."))
        return issues
    for placeholder in sorted(indexed_placeholders(root) - documented):
        issues.append(
            issue(
                "undocumented-placeholder",
                "docs/PLACEHOLDERS.md",
                f"`{placeholder}` is used by component/template metadata but is not documented.",
            )
        )
    issues.extend(accidental_angle_placeholders(root))
    return sorted(issues, key=lambda item: (item["severity"], item["path"], item["line"] or 0, item["code"], item["message"]))


def print_issues(issues):
    if not issues:
        print("Placeholder quality checks passed.")
        return
    print("Placeholder quality checks failed:")
    for item in issues[:80]:
        line = f",line={item['line']}" if item.get("line") else ""
        print(f"- [{item['severity']}] {item['path']}: {item['code']} - {item['message']}")
        print(f"::error file={item['path']}{line}::{item['code']}: {item['message']}")
    if len(issues) > 80:
        print(f"... and {len(issues) - 80} more")


def run_self_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "docs").mkdir()
        (root / "components").mkdir()
        (root / "templates" / "contracts").mkdir(parents=True)
        (root / "docs" / "PLACEHOLDERS.md").write_text("| Placeholder | Meaning |\n| --- | --- |\n| `PROJECT_NAME` | Name |\n", encoding="utf-8")
        (root / "components" / "index.json").write_text(
            json.dumps({"schemaVersion": 1, "components": [{"path": "components/x.md", "maturity": "stable", "requiredPlaceholders": ["PROJECT_NAME"]}]}),
            encoding="utf-8",
        )
        (root / "components" / "x.md").write_text("# X\n\nUse `PROJECT_NAME`.\n", encoding="utf-8")
        assert collect_placeholder_issues(root) == []
        (root / "components" / "x.md").write_text("# X\n\nUse <project name>.\n", encoding="utf-8")
        assert accidental_angle_placeholders(root)
    print("placeholder_quality.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Validate documented placeholders and stable Markdown placeholder style.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--self-test", action="store_true", help="Run focused placeholder self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    issues = collect_placeholder_issues(Path(args.repo_root).resolve())
    print_issues(issues)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
