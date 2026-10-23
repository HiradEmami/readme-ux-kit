from pathlib import Path
import argparse
import re
import tempfile

from src.modules.common.repo import (
    is_external_url,
    is_placeholder_url,
    iter_markdown_files,
    load_json,
    markdown_anchors,
    markdown_links,
    read_text,
    rel_path,
    repo_root,
    split_link_target,
)
from src.modules.indexers.component_index import check_component_index
from src.modules.indexers.template_index import check_template_index
from src.modules.markdown.placeholder_quality import collect_placeholder_issues
from src.modules.themes.theme_index import build_theme_index, validation_errors as theme_validation_errors


REQUIRED_DOCS = (
    "docs/DESIGN_SYSTEM.md",
    "docs/PLACEHOLDERS.md",
    "docs/COMPOSITION_RULES.md",
    "docs/TEMPLATE_CONTRACTS.md",
    "docs/THEME_SYSTEM.md",
    "docs/COMPONENT_AUTHORING.md",
    "docs/QUALITY_BAR.md",
    "docs/COMPATIBILITY_MATRIX.md",
    "docs/README_ARCHETYPES.md",
    "docs/ANTI_PATTERNS.md",
)
COMPATIBILITY_TEMPLATE_RE = re.compile(r"\|\s*`([^`]+)`\s*\|")
COMPATIBILITY_CODE_RE = re.compile(r"`([^`]+)`")


def issue(code, path, message, severity="error"):
    return {
        "code": code,
        "path": Path(path).as_posix() if path else "",
        "message": message,
        "severity": severity,
    }


def local_link_issues(root):
    root = Path(root)
    issues = []
    anchors_cache = {}
    for md_file in iter_markdown_files(root, ["components", "templates", "themes", *REQUIRED_DOCS]):
        if not md_file.exists():
            continue
        relative = rel_path(md_file, root)
        for target in markdown_links(md_file):
            path_text, anchor = split_link_target(target)
            if not path_text and anchor:
                if anchor not in markdown_anchors(md_file):
                    issues.append(issue("missing-anchor", relative, f"Missing local anchor #{anchor}"))
                continue
            if not path_text or is_external_url(path_text) or is_placeholder_url(path_text):
                continue
            target_path = (md_file.parent / path_text).resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                issues.append(issue("link-outside-repo", relative, f"Link points outside repository: {target}"))
                continue
            if not target_path.exists():
                issues.append(issue("missing-local-link", relative, f"Missing local link target: {target}"))
                continue
            if anchor and target_path.suffix.lower() == ".md":
                anchors = anchors_cache.setdefault(target_path, markdown_anchors(target_path))
                if anchor not in anchors:
                    issues.append(issue("missing-target-anchor", relative, f"Missing anchor #{anchor} in {rel_path(target_path, root)}"))
    return issues


def required_docs_issues(root):
    issues = []
    for relative in REQUIRED_DOCS:
        path = Path(root) / relative
        if not path.exists():
            issues.append(issue("missing-design-doc", relative, "Required design-system documentation is missing."))
        elif len(read_text(path).split()) < 40:
            issues.append(issue("thin-design-doc", relative, "Documentation is too thin to be useful as a standalone handoff.", severity="warning"))
    return issues


def compatibility_matrix_issues(root):
    root = Path(root)
    path = root / "docs" / "COMPATIBILITY_MATRIX.md"
    if not path.exists():
        return [issue("missing-compatibility-matrix", "docs/COMPATIBILITY_MATRIX.md", "Compatibility matrix is missing.")]

    template_ids = {item["id"] for item in load_json(root / "templates" / "index.json").get("templates", [])}
    component_ids = {item["id"] for item in load_json(root / "components" / "index.json").get("components", [])}
    theme_ids = {theme["id"] for theme in build_theme_index(root).get("themes", [])}
    issues = []
    for line in read_text(path).splitlines():
        template_match = COMPATIBILITY_TEMPLATE_RE.match(line)
        if not template_match:
            continue
        template_id = template_match.group(1)
        if template_id not in template_ids:
            issues.append(issue("unknown-template-reference", rel_path(path, root), f"Unknown template in matrix: {template_id}"))
        for value in COMPATIBILITY_CODE_RE.findall(line):
            if "/" in value and value not in component_ids:
                issues.append(issue("unknown-component-reference", rel_path(path, root), f"Unknown component in matrix: {value}"))
            elif "/" not in value and value not in template_ids and value not in theme_ids:
                issues.append(issue("unknown-theme-reference", rel_path(path, root), f"Unknown theme in matrix: {value}"))
    return issues


def index_and_contract_issues(root):
    root = Path(root)
    issues = []
    component_status, component_errors = check_component_index(root / "components" / "index.json", root)
    template_status, template_errors = check_template_index(root / "templates" / "index.json", root)
    if component_status:
        issues.append(issue("stale-component-index", "components/index.json", f"Component index is {component_status}."))
    if template_status:
        issues.append(issue("stale-template-index", "templates/index.json", f"Template index is {template_status}."))
    issues.extend(issue("component-index", "components/index.json", error) for error in component_errors)
    issues.extend(issue("template-index", "templates/index.json", error) for error in template_errors)
    theme_payload = build_theme_index(root)
    issues.extend(issue("theme-index", "themes/index.json", error) for error in theme_validation_errors(theme_payload, root))
    return issues


def collect_design_system_issues(root=None):
    root = Path(root or repo_root()).resolve()
    issues = []
    for check in (required_docs_issues, local_link_issues, compatibility_matrix_issues, index_and_contract_issues):
        issues.extend(check(root))
    for item in collect_placeholder_issues(root):
        issues.append(issue(item["code"], item["path"], item["message"], item["severity"]))
    return sorted(issues, key=lambda item: (item["severity"], item["path"], item["code"], item["message"]))


def print_issues(issues):
    if not issues:
        print("Design system quality checks passed.")
        return
    has_errors = any(item["severity"] == "error" for item in issues)
    print("Design system quality checks failed:" if has_errors else "Design system quality checks passed with warnings:")
    for item in issues[:100]:
        annotation = "error" if item["severity"] == "error" else "warning"
        print(f"- [{item['severity']}] {item['path']}: {item['code']} - {item['message']}")
        print(f"::{annotation} file={item['path']}::{item['code']}: {item['message']}")
    if len(issues) > 100:
        print(f"... and {len(issues) - 100} more")


def run_self_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        for directory in ("components/navigation", "templates/contracts", "themes/minimal", "docs"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        for doc in REQUIRED_DOCS:
            (root / doc).parent.mkdir(parents=True, exist_ok=True)
            (root / doc).write_text(
                "# Doc\n\n"
                "This local design-system document has enough words to behave as a useful standalone handoff for validation tests. "
                "It explains purpose, scope, usage, validation expectations, review rules, compatibility boundaries, and maintenance "
                "responsibilities clearly enough that another session can continue the work without guessing.\n",
                encoding="utf-8",
            )
        (root / "components" / "index.json").write_text('{"schemaVersion":1,"componentCount":0,"components":[],"groups":[]}', encoding="utf-8")
        (root / "templates" / "index.json").write_text('{"schemaVersion":1,"templateCount":0,"templates":[]}', encoding="utf-8")
        assert required_docs_issues(root) == []
        (root / "docs" / "COMPATIBILITY_MATRIX.md").write_text("| Template | Strong Themes | Strong Components | Asset Families |\n| --- | --- | --- | --- |\n", encoding="utf-8")
        assert compatibility_matrix_issues(root) == []
    print("design_system_quality.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Validate README design-system metadata, docs, and compatibility.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--self-test", action="store_true", help="Run focused design-system self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    issues = collect_design_system_issues(Path(args.repo_root).resolve())
    print_issues(issues)
    return 1 if any(item["severity"] == "error" for item in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
