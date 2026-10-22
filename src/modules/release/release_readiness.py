from pathlib import Path
import argparse
import json
import subprocess

from src.modules.common.repo import load_json, rel_path, repo_root


REQUIRED_SCRIPTS = (
    "check:all",
    "check:generators",
    "check:manifest",
    "check:previews",
    "check:site-data",
    "check:svg",
    "check:svg:optimize",
    "quality:gate",
    "release",
)
REQUIRED_DOCS = (
    "docs/RELEASE.md",
    "docs/CHANGELOG.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
    "SECURITY.md",
    "ACCESSIBILITY.md",
    "PRIVACY.md",
    "THIRD_PARTY_NOTICES.md",
    "ASSET_PROVENANCE.md",
    "ARCHITECTURE.md",
    "AGENTS.md",
    "AGENT.md",
    "CLAUDE.md",
    "SKILL.md",
    ".mcp.json",
    ".well-known/security.txt",
    "licenses/third-party.txt",
    ".env.example",
    ".gitattributes",
    ".nvmrc",
    ".editorconfig",
    "tsconfig.json",
    ".github/workflows/ci.yml",
)
REQUIRED_GENERATED_OUTPUTS = (
    "assets/manifest.json",
    "assets/provenance.json",
    "ASSET_PROVENANCE.json",
    "previews/assets/README.md",
    "site/data/assets.json",
    "site/data/editor-presets.json",
    "site/data/theme-palettes.json",
    "site/data/editor-capabilities.json",
    "site/data/search-index.json",
    "site/data/svg-analysis.json",
    "site/data/themes.json",
    "site/data/schema-catalog.json",
    "site/data/quality-report.json",
    "site/data/asset-packs.json",
    "site/data/compatibility-report.json",
    "site/data/migration-plan.json",
)


def problem(code, message, path="", severity="error"):
    return {"code": code, "message": message, "path": path, "severity": severity}


def package_script_issues(root):
    package_path = root / "package.json"
    if not package_path.exists():
        return [problem("missing-package-json", "package.json is required for release checks.", "package.json")]
    package = load_json(package_path)
    scripts = package.get("scripts", {})
    issues = []
    for script in REQUIRED_SCRIPTS:
        if script not in scripts:
            issues.append(problem("missing-release-script", f"Missing package script `{script}`.", "package.json"))
    if package.get("license") != "MIT":
        issues.append(problem("missing-package-license", "package.json must declare `\"license\": \"MIT\"`.", "package.json"))
    if not isinstance(package.get("engines"), dict) or "node" not in package.get("engines", {}):
        issues.append(problem("missing-package-engines", "package.json must declare `engines.node`.", "package.json"))
    return issues


def semantic_release_issues(root):
    path = root / ".releaserc.json"
    if not path.exists():
        return [problem("missing-semantic-release-config", ".releaserc.json is required.", ".releaserc.json")]
    try:
        config = load_json(path)
    except json.JSONDecodeError as error:
        return [problem("invalid-semantic-release-config", str(error), ".releaserc.json")]
    issues = []
    branches = config.get("branches", [])
    branch_names = {branch if isinstance(branch, str) else branch.get("name") for branch in branches}
    if not {"master", "main"} & branch_names:
        issues.append(problem("missing-release-branch", "semantic-release should declare master or main as a release branch.", ".releaserc.json"))
    if not config.get("plugins"):
        issues.append(problem("missing-release-plugins", "semantic-release plugins are not configured.", ".releaserc.json"))
    return issues


def docs_issues(root):
    issues = []
    for doc in REQUIRED_DOCS:
        path = root / doc
        if not path.exists():
            issues.append(problem("missing-release-doc", f"{doc} is required.", doc))
    if (root / "docs" / "RELEASE.md").exists() and "npm run check:all" not in (root / "docs" / "RELEASE.md").read_text(encoding="utf-8"):
        issues.append(problem("release-doc-missing-check-all", "Release docs should require npm run check:all.", "docs/RELEASE.md"))
    if (root / "docs" / "CHANGELOG.md").exists() and "Generated Output Rules" not in (root / "docs" / "CHANGELOG.md").read_text(encoding="utf-8"):
        issues.append(problem("changelog-doc-missing-generated-rules", "Changelog docs should document generated output rules.", "docs/CHANGELOG.md"))
    if (root / "CHANGELOG.md").exists() and len((root / "CHANGELOG.md").read_text(encoding="utf-8").strip()) < 100:
        issues.append(problem("empty-root-changelog", "Root CHANGELOG.md must contain structured release history.", "CHANGELOG.md"))
    return issues


def generated_output_issues(root):
    return [
        problem("missing-generated-output", f"Generated output is missing: {path}", path)
        for path in REQUIRED_GENERATED_OUTPUTS
        if not (root / path).exists()
    ]


def dirty_worktree_issues(root, strict=False):
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=root, text=True, capture_output=True, check=False)
    except OSError as error:
        return [problem("git-status-unavailable", str(error), severity="warning")]
    if result.returncode != 0:
        return [problem("git-status-failed", result.stderr.strip() or "git status failed", severity="warning")]
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        return []
    severity = "error" if strict else "warning"
    return [problem("dirty-worktree", f"Worktree has {len(lines)} uncommitted change(s).", severity=severity)]


def parse_semantic_release_dry_run(text):
    lowered = text.lower()
    return {
        "hasNextRelease": "next release version is" in lowered or "published release" in lowered,
        "hasNoRelease": "no relevant changes" in lowered or "no release is necessary" in lowered,
        "hasError": "error" in lowered or "failed" in lowered,
    }


def collect_release_issues(root=None, strict_worktree=False):
    root = Path(root or repo_root()).resolve()
    issues = []
    for check in [package_script_issues, semantic_release_issues, docs_issues, generated_output_issues]:
        issues.extend(check(root))
    issues.extend(dirty_worktree_issues(root, strict=strict_worktree))
    return sorted(issues, key=lambda item: (item["severity"], item.get("path", ""), item["code"]))


def print_issues(issues):
    if not issues:
        print("Release readiness checks passed.")
        return
    has_errors = any(item["severity"] == "error" for item in issues)
    print("Release readiness checks failed:" if has_errors else "Release readiness checks passed with warnings:")
    for item in issues:
        prefix = "error" if item["severity"] == "error" else "warning"
        path = item.get("path") or "release"
        print(f"- [{item['severity']}] {path}: {item['code']} - {item['message']}")
        print(f"::{prefix} file={path}::{item['code']}: {item['message']}")


def run_self_tests():
    parsed = parse_semantic_release_dry_run("The next release version is 1.2.3")
    assert parsed["hasNextRelease"]
    parsed = parse_semantic_release_dry_run("There are no relevant changes, so no new version is released.")
    assert parsed["hasNoRelease"]
    print("release_readiness.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Check release readiness for docs, generated files, scripts, and semantic-release config.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--strict-worktree", action="store_true", help="Fail when the worktree is dirty.")
    parser.add_argument("--self-test", action="store_true", help="Run focused release checker self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    issues = collect_release_issues(root, strict_worktree=args.strict_worktree)
    print_issues(issues)
    return 1 if any(item["severity"] == "error" for item in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
