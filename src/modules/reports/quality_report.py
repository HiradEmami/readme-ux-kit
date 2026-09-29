from pathlib import Path
import argparse
import json

from src.modules.common.repo import load_json, rel_path, repo_root, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/reports/quality_report.py"


def safe_load(path, default):
    path = Path(path)
    if not path.exists():
        return default
    return load_json(path)


def top_paths(items, key, limit=10):
    return [
        {
            "path": item.get("path"),
            "name": item.get("name"),
            key: item.get(key),
            "flags": item.get("flags", []),
        }
        for item in sorted(items, key=lambda item: item.get(key, 0), reverse=True)[:limit]
    ]


def build_quality_report(root=None):
    root = Path(root or repo_root()).resolve()
    manifest = safe_load(root / "assets" / "manifest.json", {"assets": [], "categoryCounts": {}})
    analysis = safe_load(root / "site" / "data" / "svg-analysis.json", {"summary": {}, "assets": []})
    themes = safe_load(root / "themes" / "index.json", {"themes": []})
    provenance = safe_load(root / "assets" / "provenance.json", {"summary": {}})
    recipes = safe_load(root / "site" / "data" / "recipes.json", {"recipes": []})
    bundles = safe_load(root / "site" / "data" / "bundles.json", {"bundles": []})
    compatibility = safe_load(root / "site" / "data" / "compatibility-report.json", {"summary": {}})

    theme_warnings = [
        {"id": theme["id"], "warnings": theme.get("status", {}).get("warnings", [])}
        for theme in themes.get("themes", [])
        if theme.get("status", {}).get("warnings")
    ]
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "summary": {
            "assetCount": manifest.get("assetCount", len(manifest.get("assets", []))),
            "categoryCounts": manifest.get("categoryCounts", {}),
            "themeCount": themes.get("themeCount", len(themes.get("themes", []))),
            "recipeCount": recipes.get("recipeCount", len(recipes.get("recipes", []))),
            "bundleCount": bundles.get("bundleCount", len(bundles.get("bundles", []))),
            "provenance": provenance.get("summary", {}),
            "svgFlagCounts": analysis.get("summary", {}).get("flagCounts", {}),
            "compatibility": compatibility.get("summary", {}),
        },
        "topAssets": {
            "largest": top_paths(analysis.get("assets", []), "fileSize"),
            "mostComplex": top_paths(analysis.get("assets", []), "complexityScore"),
            "highestMotion": top_paths(analysis.get("assets", []), "motionScore"),
        },
        "themeWarnings": theme_warnings,
        "reviewChecklist": [
            "Run npm run check:all before release.",
            "Preview generated Markdown on GitHub when adding new HTML patterns.",
            "Review high-motion and high-complexity SVGs before promoting them in README examples.",
            "Update third-party provenance when adding externally sourced assets.",
        ],
    }


def markdown_report(payload):
    summary = payload["summary"]
    lines = [
        "# README UX Kit Quality Report",
        "",
        "Generated from repository manifests and analysis data.",
        "",
        "## Summary",
        "",
        f"- Assets: {summary.get('assetCount', 0)}",
        f"- Themes: {summary.get('themeCount', 0)}",
        f"- Recipes: {summary.get('recipeCount', 0)}",
        f"- Copy-all bundles: {summary.get('bundleCount', 0)}",
        f"- Provenance origins: {summary.get('provenance', {}).get('originCounts', {})}",
        "",
        "## SVG Signals",
        "",
    ]
    flag_counts = summary.get("svgFlagCounts", {})
    if flag_counts:
        lines.extend(f"- {flag}: {count}" for flag, count in sorted(flag_counts.items()))
    else:
        lines.append("- No SVG flags reported.")
    lines.extend(["", "## Largest Assets", "", "| Asset | Size | Flags |", "| --- | ---: | --- |"])
    for asset in payload["topAssets"]["largest"][:10]:
        lines.append(f"| `{asset['path']}` | {asset.get('fileSize', 0)} | {', '.join(asset.get('flags', [])) or 'none'} |")
    lines.extend(["", "## Review Checklist", ""])
    lines.extend(f"- {item}" for item in payload["reviewChecklist"])
    return "\n".join(lines) + "\n"


def write_reports(json_output, markdown_output, root=None):
    payload = build_quality_report(root)
    json_path = write_json(json_output, payload)
    markdown_output = Path(markdown_output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(markdown_report(payload), encoding="utf-8")
    return json_path, markdown_output


def check_reports(json_output, markdown_output, root=None):
    payload = build_quality_report(root)
    expected_json = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    expected_md = markdown_report(payload)
    failures = []
    for path, expected in [(Path(json_output), expected_json), (Path(markdown_output), expected_md)]:
        if not path.exists():
            failures.append((path, "missing"))
        elif path.read_text(encoding="utf-8") != expected:
            failures.append((path, "changed"))
    return failures


def run_self_tests():
    payload = build_quality_report()
    assert "summary" in payload
    assert "reviewChecklist" in payload
    assert markdown_report(payload).startswith("# README UX Kit Quality Report")
    print("quality_report.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate repository quality reports.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="site/data/quality-report.json", help="Quality report JSON path relative to repo root.")
    parser.add_argument("--markdown-output", default="site/reports/quality-report.md", help="Quality report Markdown path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify quality reports are current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused report self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    markdown_output = root / args.markdown_output
    if args.check:
        failures = check_reports(output, markdown_output, root)
        for path, status in failures:
            print(f"::error file={rel_path(path, root)}::Quality report is {status}. Run npm run generate:reports.")
        if failures:
            return 1
        print("Quality reports are current.")
        return 0

    json_path, md_path = write_reports(output, markdown_output, root)
    print(f"Wrote quality report to {json_path}")
    print(f"Wrote Markdown quality report to {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
