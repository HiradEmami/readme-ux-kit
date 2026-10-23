from pathlib import Path
import re
import tempfile

from src.modules.common.repo import (
    is_external_url,
    is_placeholder_url,
    iter_markdown_files,
    iter_svg_files,
    markdown_anchors,
    markdown_links,
    read_text,
    rel_path,
    repo_root,
    split_link_target,
)
from src.modules.generators.validate_svg_assets import validate_svg


RAW_BASE = "https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/"
EXPECTED_THEME_FILES = (
    "example.md",
    "colors.md",
    "assets-map.md",
    "tokens.json",
    "usage.md",
    "voice.md",
    "components.md",
    "template-matrix.md",
    "contrast.md",
    "preview.md",
)
ALLOWED_TEMPLATE_PLACEHOLDERS = {
    "API_TOKEN",
    "BROWSER_SUPPORT",
    "BUILD_COMMAND",
    "BOUNDARY",
    "BUSINESS_CAPABILITY",
    "CLIENT_SYSTEMS",
    "COMMON_PAIN_POINT",
    "COMMON_WORKAROUND",
    "CORE_RESPONSIBILITY",
    "DATABASE_NAME",
    "DATABASE_URL",
    "DATASET_VERSION",
    "DEPLOY_COMMAND",
    "DOCS_URL",
    "ERROR_RATE_TARGET",
    "EXPLICIT_NON_GOAL_ONE",
    "EXPLICIT_NON_GOAL_TWO",
    "INSTALL_COMMAND",
    "INTEGRATION_TEST_COMMAND",
    "ISSUES_URL",
    "LANGUAGE_FRAMEWORK",
    "LINT_COMMAND",
    "LOG_LEVEL",
    "MODEL_NAME",
    "NODE_VERSION",
    "OBSERVABILITY_STACK",
    "OWNER",
    "P95_LATENCY_TARGET",
    "PACKAGE_NAME",
    "PACKAGE_ECOSYSTEM",
    "PRIMARY_API",
    "PRIMARY_DATA",
    "PRIMARY_DOMAIN",
    "PRIMARY_OUTCOME",
    "PRIMARY_PROBLEM",
    "PRODUCTION_URL",
    "PROJECT_ENV",
    "PROJECT_LOG_LEVEL",
    "QUEUE_URL",
    "QUEUE_LAG_TARGET",
    "QUEUE_NAME",
    "PROJECT_NAME",
    "REPO",
    "RESPONSIBILITY_ONE",
    "RESPONSIBILITY_THREE",
    "RESPONSIBILITY_TWO",
    "RUN_COMMAND",
    "SCALING_OR_MAINTENANCE_ISSUE",
    "SECURITY_CONTACT",
    "SERVICE_NAME",
    "START_DEPENDENCIES_COMMAND",
    "STAGING_URL",
    "STORAGE_LAYER",
    "SUPPORT_URL",
    "TASK_NAME",
    "TEAM_NAME",
    "TARGET_USER",
    "TEST_COMMAND",
    "UNIT_TEST_COMMAND",
}
PLACEHOLDER_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")


def issue(code, path, message, severity="error"):
    return {
        "code": code,
        "path": Path(path).as_posix() if path else "",
        "message": message,
        "severity": severity,
    }


def local_markdown_link_issues(root):
    issues = []
    roots = [
        "README.md",
        "NAVIGATION.md",
        "CONTRIBUTING.md",
        "docs",
        "components",
        "templates",
        "themes",
        "previews/assets",
    ]

    for md_file in iter_markdown_files(root, roots):
        anchors_cache = {}
        for target in markdown_links(md_file):
            path_text, anchor = split_link_target(target)
            if not path_text and anchor:
                if anchor not in markdown_anchors(md_file):
                    issues.append(issue("missing-anchor", rel_path(md_file, root), f"Missing local anchor #{anchor}"))
                continue
            if not path_text or is_external_url(path_text) or is_placeholder_url(path_text):
                continue
            target_path = (md_file.parent / path_text).resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                issues.append(issue("link-outside-repo", rel_path(md_file, root), f"Link points outside repository: {target}"))
                continue
            if not target_path.exists():
                issues.append(issue("missing-local-link", rel_path(md_file, root), f"Missing local link target: {target}"))
                continue
            if anchor and target_path.suffix.lower() == ".md":
                anchors = anchors_cache.setdefault(target_path, markdown_anchors(target_path))
                if anchor not in anchors:
                    issues.append(
                        issue(
                            "missing-target-anchor",
                            rel_path(md_file, root),
                            f"Missing anchor #{anchor} in {rel_path(target_path, root)}",
                        )
                    )
    return issues


def raw_asset_url_issues(root):
    issues = []
    for md_file in iter_markdown_files(root, ["README.md", "docs", "components", "templates", "themes", "previews/assets"]):
        for target in markdown_links(md_file):
            if not target.startswith(RAW_BASE):
                continue
            local = target[len(RAW_BASE) :].split("#", 1)[0].split("?", 1)[0]
            if is_placeholder_url(local):
                continue
            local_path = root / local
            if not local_path.exists():
                issues.append(issue("missing-raw-asset", rel_path(md_file, root), f"Raw GitHub URL has no local file: {target}"))
    return issues


def template_placeholder_issues(root):
    issues = []
    for template in sorted((root / "templates").glob("*.md"), key=lambda path: path.name.lower()):
        if template.name == "README.md":
            continue
        content = read_text(template)
        tokens = set(PLACEHOLDER_RE.findall(content))
        unknown = sorted(token for token in tokens if token not in ALLOWED_TEMPLATE_PLACEHOLDERS and token.endswith(("_NAME", "_TOKEN", "_URL")))
        for token in unknown:
            issues.append(issue("unknown-template-placeholder", rel_path(template, root), f"Unexpected placeholder token: {token}"))
        if "PROJECT_NAME" not in tokens and "SERVICE_NAME" not in tokens:
            issues.append(
                issue(
                    "missing-template-title-placeholder",
                    rel_path(template, root),
                    "Template should include PROJECT_NAME or SERVICE_NAME when it is intended as a direct paste starter.",
                    severity="warning",
                )
            )
    return issues


def theme_completeness_issues(root):
    issues = []
    for theme_dir in sorted((root / "themes").iterdir(), key=lambda path: path.name.lower()):
        if not theme_dir.is_dir():
            continue
        for filename in EXPECTED_THEME_FILES:
            target = theme_dir / filename
            if not target.exists():
                issues.append(issue("missing-theme-file", rel_path(theme_dir, root), f"Theme is missing {filename}"))
        assets_map = theme_dir / "assets-map.md"
        if assets_map.exists():
            for target in markdown_links(assets_map):
                path_text, _ = split_link_target(target)
                if not path_text or is_external_url(path_text) or is_placeholder_url(path_text):
                    continue
                if not (assets_map.parent / path_text).resolve().exists():
                    issues.append(issue("missing-theme-asset-link", rel_path(assets_map, root), f"Missing theme asset link: {target}"))
    return issues


def svg_safety_issues(root):
    issues = []
    for svg_file in iter_svg_files(root / "assets"):
        for message in validate_svg(svg_file):
            issues.append(issue("svg-safety", rel_path(svg_file, root), message))
    return issues


def collect_quality_issues(root=None):
    root = Path(root or repo_root()).resolve()
    checks = [
        local_markdown_link_issues,
        raw_asset_url_issues,
        template_placeholder_issues,
        theme_completeness_issues,
        svg_safety_issues,
    ]
    issues = []
    for check in checks:
        issues.extend(check(root))
    return sorted(issues, key=lambda item: (item["severity"], item["path"], item["code"], item["message"]))


def print_issues(issues):
    if not issues:
        print("Repository quality checks passed.")
        return
    has_errors = any(item["severity"] == "error" for item in issues)
    print("Repository quality checks failed:" if has_errors else "Repository quality checks passed with warnings:")
    print()
    for item in issues[:80]:
        print(f"- [{item['severity']}] {item['path']}: {item['code']} - {item['message']}")
        if item["severity"] == "error":
            print(f"::error file={item['path']}::{item['code']}: {item['message']}")
        else:
            print(f"::warning file={item['path']}::{item['code']}: {item['message']}")
    if len(issues) > 80:
        print(f"... and {len(issues) - 80} more")


def run_self_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "templates").mkdir()
        (root / "themes" / "minimal").mkdir(parents=True)
        (root / "assets").mkdir()
        (root / "README.md").write_text("# Demo\n\n[Local](./docs/page.md)\n", encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs" / "page.md").write_text("# Page\n", encoding="utf-8")
        (root / "templates" / "minimal.md").write_text("# PROJECT_NAME\n", encoding="utf-8")
        for name in EXPECTED_THEME_FILES:
            (root / "themes" / "minimal" / name).write_text("# Minimal\n", encoding="utf-8")
        assert local_markdown_link_issues(root) == []
        assert template_placeholder_issues(root) == []
        assert theme_completeness_issues(root) == []
        (root / "README.md").write_text("[Missing](./docs/missing.md)\n", encoding="utf-8")
        assert local_markdown_link_issues(root)
    print("repo_quality.py self-tests passed.")
