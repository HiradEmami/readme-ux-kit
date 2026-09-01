import argparse
from pathlib import Path

from src.modules.common.repo import load_json, repo_root


def generate_all(root):
    from src.modules.analyzers.svg_analysis import write_analysis
    from src.modules.compatibility.github_markdown import write_compatibility_report
    from src.modules.editor.svg_editor import write_capabilities
    from src.modules.generators.asset_manifest import write_manifest
    from src.modules.generators.editor_presets import write_editor_data
    from src.modules.indexers.search_index import write_indexes
    from src.modules.markdown.markdown_quality import write_snippets
    from src.modules.migrations.migration_registry import write_plan
    from src.modules.packagers.asset_packs import write_asset_packs
    from src.modules.provenance.provenance_index import write_provenance
    from src.modules.recipes.recipe_index import write_recipe_indexes
    from src.modules.reports.quality_report import write_reports
    from src.modules.renderers.svg_smoke_render import write_smoke_outputs
    from src.modules.schemas.schema_registry import write_catalog
    from src.modules.themes.theme_index import write_theme_indexes

    root = Path(root).resolve()
    write_manifest(root, Path("assets"), root / "assets" / "manifest.json")
    write_manifest(root, Path("assets"), root / "site" / "data" / "assets.json")
    write_editor_data(root / "site" / "data")
    write_capabilities(root / "site" / "data" / "editor-capabilities.json")
    write_theme_indexes(root / "themes" / "index.json", root / "site" / "data" / "themes.json", root)
    write_analysis(root / "site" / "data" / "svg-analysis.json", root, root / "assets" / "manifest.json")
    write_indexes(root / "site" / "data", root, root / "assets" / "manifest.json")
    write_snippets(root / "site" / "data" / "markdown-snippets.json")
    write_provenance(root / "assets" / "provenance.json", root, root / "assets" / "manifest.json")
    write_recipe_indexes(root / "site" / "data", root)
    write_smoke_outputs(root / "site" / "data" / "svg-render-smoke.json", root / "site" / "svg-contact-sheet.html", root, root / "assets" / "manifest.json")
    write_compatibility_report(root / "site" / "data" / "compatibility-report.json", root)
    write_asset_packs(root / "site" / "data" / "asset-packs.json", root / "site" / "packages" / "README.md", root)
    write_reports(root / "site" / "data" / "quality-report.json", root / "site" / "reports" / "quality-report.md", root)
    write_plan(root / "site" / "data" / "migration-plan.json", root)
    write_catalog(root / "site" / "data" / "schema-catalog.json", root)
    print("Generated module outputs.")
    return 0


def record_failure(failures, label, message):
    failures.append((label, message))
    print(f"::error::{label}: {message}")


def check_all(root):
    from src.modules.analyzers.svg_analysis import check_analysis
    from src.modules.compatibility.github_markdown import check_compatibility_report
    from src.modules.editor.svg_editor import check_capabilities
    from src.modules.generators.asset_manifest import check_manifest
    from src.modules.generators.editor_presets import check_editor_data
    from src.modules.generators.generate_asset_previews import DEFAULT_PROFILE_URL, DEFAULT_REPO_RAW_BASE, check_previews
    from src.modules.indexers.search_index import check_indexes
    from src.modules.markdown.markdown_quality import check_snippets, collect_markdown_issues
    from src.modules.migrations.migration_registry import check_plan
    from src.modules.packagers.asset_packs import check_asset_packs
    from src.modules.provenance.provenance_index import check_provenance
    from src.modules.recipes.recipe_index import check_recipe_indexes
    from src.modules.release.release_readiness import collect_release_issues
    from src.modules.reports.quality_report import check_reports
    from src.modules.renderers.svg_smoke_render import check_smoke_outputs
    from src.modules.schemas.schema_registry import check_catalog
    from src.modules.site.site_checks import collect_site_issues
    from src.modules.themes.theme_index import check_theme_indexes
    from src.modules.validators.repo_quality import collect_quality_issues

    root = Path(root).resolve()
    failures = []
    for output in [root / "assets" / "manifest.json", root / "site" / "data" / "assets.json"]:
        status, errors = check_manifest(root, Path("assets"), output)
        if status:
            record_failure(failures, "manifest", f"{output} is {status}")
        for error in errors:
            record_failure(failures, "manifest", error)

    editor_failures = check_editor_data(root / "site" / "data")
    for path, status, _errors in editor_failures:
        record_failure(failures, "editor-data", f"{path} is {status}")
    editor_status = check_capabilities(root / "site" / "data" / "editor-capabilities.json")
    if editor_status:
        record_failure(failures, "editor", f"editor capabilities are {editor_status}")

    missing, changed, extra = check_previews(root, Path("assets"), root / "previews" / "assets", DEFAULT_REPO_RAW_BASE, DEFAULT_PROFILE_URL)
    if missing or changed or extra:
        record_failure(failures, "previews", f"{len(missing)} missing, {len(changed)} changed, {len(extra)} extra")

    for label, status in [
        ("svg-analysis", check_analysis(root / "site" / "data" / "svg-analysis.json", root, root / "assets" / "manifest.json")),
        ("markdown-snippets", check_snippets(root / "site" / "data" / "markdown-snippets.json")),
    ]:
        if status:
            record_failure(failures, label, f"output is {status}")

    for path, status in check_indexes(root / "site" / "data", root, root / "assets" / "manifest.json"):
        record_failure(failures, "indexes", f"{path} is {status}")

    theme_failures, theme_errors = check_theme_indexes(root / "themes" / "index.json", root / "site" / "data" / "themes.json", root)
    for path, status in theme_failures:
        record_failure(failures, "themes", f"{path} is {status}")
    for error in theme_errors:
        record_failure(failures, "themes", error)

    provenance_status, provenance_errors = check_provenance(root / "assets" / "provenance.json", root, root / "assets" / "manifest.json")
    if provenance_status:
        record_failure(failures, "provenance", f"output is {provenance_status}")
    for error in provenance_errors:
        record_failure(failures, "provenance", error)

    recipe_failures, recipe_errors = check_recipe_indexes(root / "site" / "data", root)
    for path, status in recipe_failures:
        record_failure(failures, "recipes", f"{path} is {status}")
    for error in recipe_errors:
        record_failure(failures, "recipes", error)

    render_failures, render_errors = check_smoke_outputs(root / "site" / "data" / "svg-render-smoke.json", root / "site" / "svg-contact-sheet.html", root, root / "assets" / "manifest.json")
    for path, status in render_failures:
        record_failure(failures, "render-smoke", f"{path} is {status}")
    for asset in render_errors:
        record_failure(failures, "render-smoke", f"{asset['path']} has flags {', '.join(asset['flags'])}")

    compatibility_status, compatibility_errors = check_compatibility_report(root / "site" / "data" / "compatibility-report.json", root)
    if compatibility_status:
        record_failure(failures, "compatibility", f"output is {compatibility_status}")
    for item in compatibility_errors:
        record_failure(failures, "compatibility", f"{item['path']}: {item['code']} - {item['message']}")

    pack_failures, pack_errors = check_asset_packs(root / "site" / "data" / "asset-packs.json", root / "site" / "packages" / "README.md", root)
    for path, status in pack_failures:
        record_failure(failures, "packs", f"{path} is {status}")
    for error in pack_errors:
        record_failure(failures, "packs", error)

    report_failures = check_reports(root / "site" / "data" / "quality-report.json", root / "site" / "reports" / "quality-report.md", root)
    for path, status in report_failures:
        record_failure(failures, "reports", f"{path} is {status}")

    migration_status, migration_errors = check_plan(root / "site" / "data" / "migration-plan.json", root)
    if migration_status:
        record_failure(failures, "migrations", f"migration plan is {migration_status}")
    for error in migration_errors:
        record_failure(failures, "migrations", error)

    schema_status, schema_errors = check_catalog(root / "site" / "data" / "schema-catalog.json", root)
    if schema_status:
        record_failure(failures, "schemas", f"schema catalog is {schema_status}")
    for error in schema_errors:
        record_failure(failures, "schemas", error)

    for source, issues in [
        ("markdown", collect_markdown_issues(root)),
        ("site", collect_site_issues(root)),
        ("quality", collect_quality_issues(root)),
        ("release", collect_release_issues(root)),
    ]:
        for item in issues:
            if item["severity"] == "error":
                record_failure(failures, source, f"{item.get('path', '')}: {item['code']} - {item['message']}")

    if failures:
        print(f"Module checks failed with {len(failures)} issue(s).")
        return 1
    print("Module checks passed.")
    return 0


def report(root):
    root = Path(root).resolve()
    manifest = load_json(root / "assets" / "manifest.json")
    print(f"Assets: {manifest.get('assetCount', len(manifest.get('assets', [])))}")
    for path in [
        root / "themes" / "index.json",
        root / "site" / "data" / "templates.json",
        root / "site" / "data" / "components.json",
        root / "site" / "data" / "recipes.json",
        root / "site" / "data" / "bundles.json",
        root / "site" / "data" / "asset-packs.json",
        root / "site" / "data" / "quality-report.json",
        root / "site" / "data" / "compatibility-report.json",
    ]:
        if path.exists():
            payload = load_json(path)
            count_key = next((key for key in payload if key.endswith("Count")), None)
            print(f"{path.relative_to(root).as_posix()}: {payload.get(count_key, 'n/a')}")
    return 0


def run_self_tests():
    assert callable(generate_all)
    assert callable(check_all)
    assert callable(report)
    print("src.modules.cli self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Unified readme-ux-kit module command interface.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--self-test", action="store_true", help="Run focused CLI self-tests and exit.")
    parser.add_argument("command", nargs="?", choices=["generate", "check", "report"], default="check")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root or repo_root()).resolve()
    if args.command == "generate":
        return generate_all(root)
    if args.command == "report":
        return report(root)
    return check_all(root)


if __name__ == "__main__":
    raise SystemExit(main())
