from pathlib import Path
import argparse
import json
import re

from src.modules.common.repo import load_json, rel_path, repo_root


REQUIRED_SITE_DATA = (
    "assets.json",
    "editor-presets.json",
    "theme-palettes.json",
    "editor-capabilities.json",
    "search-index.json",
    "templates.json",
    "components.json",
    "tag-index.json",
    "svg-analysis.json",
    "markdown-snippets.json",
    "themes.json",
    "recipes.json",
    "bundles.json",
    "svg-render-smoke.json",
    "schema-catalog.json",
    "quality-report.json",
    "asset-packs.json",
    "compatibility-report.json",
    "migration-plan.json",
)
REQUIRED_STATIC_SITE_FILES = ("index.html", "styles.css", "app.js")
BACKEND_EXTENSIONS = {".py", ".php", ".rb", ".go", ".rs", ".java", ".cs"}
ROOT_RELATIVE_REFERENCE_RE = re.compile(r"""(?:href|src)=["']/""", re.IGNORECASE)
LOCAL_RUNTIME_PATTERNS = ("/api/", "localhost", "127.0.0.1", "src/app")


def issue(code, path, message, severity="error"):
    return {"code": code, "path": path, "message": message, "severity": severity}


def json_file_issues(root):
    issues = []
    data_dir = root / "site" / "data"
    if not data_dir.exists():
        return [issue("missing-site-data-dir", "site/data", "site/data is required for frontend-only browsing.")]
    for filename in REQUIRED_SITE_DATA:
        path = data_dir / filename
        if not path.exists():
            issues.append(issue("missing-site-data", rel_path(path, root), f"Missing generated site data file: {filename}"))
            continue
        try:
            payload = load_json(path)
        except json.JSONDecodeError as error:
            issues.append(issue("invalid-site-json", rel_path(path, root), str(error)))
            continue
        if "schemaVersion" not in payload:
            issues.append(issue("missing-schema-version", rel_path(path, root), "Generated site JSON should include schemaVersion."))
    return issues


def parity_issues(root):
    issues = []
    assets = root / "assets" / "manifest.json"
    site_assets = root / "site" / "data" / "assets.json"
    if assets.exists() and site_assets.exists() and assets.read_text(encoding="utf-8") != site_assets.read_text(encoding="utf-8"):
        issues.append(issue("site-assets-out-of-sync", "site/data/assets.json", "site/data/assets.json should match assets/manifest.json."))
    theme_index = root / "themes" / "index.json"
    site_themes = root / "site" / "data" / "themes.json"
    if theme_index.exists() and site_themes.exists() and theme_index.read_text(encoding="utf-8") != site_themes.read_text(encoding="utf-8"):
        issues.append(issue("site-themes-out-of-sync", "site/data/themes.json", "site/data/themes.json should match themes/index.json."))
    return issues


def frontend_only_issues(root):
    issues = []
    site_dir = root / "site"
    if not site_dir.exists():
        return [issue("missing-site-dir", "site", "site directory is required for static data output.")]
    for filename in REQUIRED_STATIC_SITE_FILES:
        path = site_dir / filename
        if not path.exists():
            issues.append(issue("missing-static-site-file", rel_path(path, root), f"Missing static showcase file: {filename}"))
    for path in site_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in BACKEND_EXTENSIONS:
            issues.append(issue("backend-file-in-site", rel_path(path, root), "The site lane should stay frontend-only/static."))
    if (site_dir / "package.json").exists():
        issues.append(issue("site-package-json", "site/package.json", "Keep the site lane static unless a future task introduces a frontend build step."))
    if not any((site_dir / name).exists() for name in ["index.html", "svg-contact-sheet.html"]):
        issues.append(issue("missing-static-site-entry", "site", "Add index.html or a generated contact sheet before deploying the site.", severity="warning"))
    return issues


def static_shell_issues(root):
    issues = []
    site_dir = root / "site"
    index_path = site_dir / "index.html"
    app_path = site_dir / "app.js"
    if not index_path.exists() or not app_path.exists():
        return issues

    index_text = index_path.read_text(encoding="utf-8")
    app_text = app_path.read_text(encoding="utf-8")
    if 'href="./styles.css"' not in index_text:
        issues.append(issue("missing-site-css-reference", "site/index.html", "site/index.html should reference ./styles.css."))
    if 'src="./app.js"' not in index_text:
        issues.append(issue("missing-site-js-reference", "site/index.html", "site/index.html should reference ./app.js."))
    if './data/assets.json' not in app_text:
        issues.append(issue("missing-site-data-fetch", "site/app.js", "site/app.js should read generated assets from ./data/assets.json."))
    if 'sourceTreeSite ? "../" : "./"' not in app_text:
        issues.append(issue("missing-site-asset-resolution", "site/app.js", "Resolve assets from the repository root in source mode and from the bundled artifact in Pages mode."))
    if "triggerDownload(item.rawUrl" in app_text:
        issues.append(issue("remote-site-asset-fallback", "site/app.js", "Downloads must use bundled local assets rather than silently depending on raw GitHub URLs."))
    if ROOT_RELATIVE_REFERENCE_RE.search(index_text):
        issues.append(issue("root-relative-site-reference", "site/index.html", "Use relative href/src paths so GitHub Project Pages work under /readme-ux-kit/."))
    for pattern in LOCAL_RUNTIME_PATTERNS:
        if pattern in index_text or pattern in app_text:
            issues.append(issue("local-runtime-reference", "site", f"The static site must not depend on `{pattern}` at runtime."))
    if "http.server" in index_text or "http.server" in app_text:
        issues.append(issue("server-runtime-reference", "site", "The deployed showcase should not require a server runtime."))
    return issues


def pages_workflow_issues(root):
    issues = []
    path = root / ".github" / "workflows" / "pages.yml"
    if not path.exists():
        return [issue("missing-pages-workflow", ".github/workflows/pages.yml", "Add a GitHub Pages workflow that uploads the static site artifact.")]

    text = path.read_text(encoding="utf-8")
    required = {
        "actions/upload-pages-artifact": "Workflow should upload a GitHub Pages artifact.",
        "actions/deploy-pages": "Workflow should deploy through GitHub Pages.",
        "npm run build:pages": "Workflow should build a self-contained Pages artifact.",
        "path: build/pages": "Workflow should upload the self-contained Pages artifact.",
        "npm run check:site": "Workflow should validate the static site before deployment.",
        "npm run check:pages": "Workflow should validate bundled local assets before deployment.",
    }
    for token, message in required.items():
        if token not in text:
            issues.append(issue("incomplete-pages-workflow", ".github/workflows/pages.yml", message))
    return issues


def collect_site_issues(root=None):
    root = Path(root or repo_root()).resolve()
    issues = []
    for check in [json_file_issues, parity_issues, frontend_only_issues, static_shell_issues, pages_workflow_issues]:
        issues.extend(check(root))
    return sorted(issues, key=lambda item: (item["severity"], item["path"], item["code"]))


def print_issues(issues):
    if not issues:
        print("Static site data checks passed.")
        return
    print("Static site data issues:")
    for item in issues:
        prefix = "error" if item["severity"] == "error" else "warning"
        print(f"- [{item['severity']}] {item['path']}: {item['code']} - {item['message']}")
        print(f"::{prefix} file={item['path']}::{item['code']}: {item['message']}")


def run_self_tests():
    assert "assets.json" in REQUIRED_SITE_DATA
    assert "index.html" in REQUIRED_STATIC_SITE_FILES
    assert ".py" in BACKEND_EXTENSIONS
    assert ROOT_RELATIVE_REFERENCE_RE.search('<script src="/app.js"></script>')
    assert not ROOT_RELATIVE_REFERENCE_RE.search('<script src="./app.js"></script>')
    app_text = 'const sourceTreeSite = true; return `${sourceTreeSite ? "../" : "./"}${item.path}`;'
    assert 'sourceTreeSite ? "../" : "./"' in app_text
    assert "triggerDownload(item.rawUrl" not in app_text
    assert "pages_workflow_issues" in globals()
    workflow = "npm run build:pages\nnpm run check:site\nnpm run check:pages\npath: build/pages\nactions/upload-pages-artifact\nactions/deploy-pages"
    assert all(token in workflow for token in ("npm run build:pages", "npm run check:pages", "path: build/pages"))
    print("site_checks.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Validate frontend-only static site data.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--self-test", action="store_true", help="Run focused site checker self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    issues = collect_site_issues(root)
    print_issues(issues)
    return 1 if any(item["severity"] == "error" for item in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
