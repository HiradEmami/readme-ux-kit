from pathlib import Path
import argparse
import json

from src.modules.common.repo import load_json, rel_path, repo_root, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/packagers/asset_packs.py"


def asset_snippet(asset):
    return {
        "path": asset["localPath"],
        "name": asset["name"],
        "rawUrl": asset["rawUrl"],
        "markdown": f"[![{asset['name']}]({asset['rawUrl']})](https://github.com/HiradEmami/readme-ux-kit)",
        "html": f'<img alt="{asset["name"]}" src="{asset["rawUrl"]}">',
        "tags": asset.get("tags", []),
    }


def category_packs(manifest):
    packs = []
    by_category = {}
    for asset in manifest["assets"]:
        by_category.setdefault(asset["category"], []).append(asset)
    for category, assets in sorted(by_category.items()):
        packs.append(
            {
                "id": f"category-{category}",
                "type": "category",
                "title": f"{category.replace('_', ' ').title()} Asset Pack",
                "description": f"All {category.replace('_', ' ')} assets with raw URLs and copy snippets.",
                "assetCount": len(assets),
                "assets": [asset_snippet(asset) for asset in sorted(assets, key=lambda item: item["localPath"])],
                "sourcePath": "assets/manifest.json",
            }
        )
    return packs


def theme_packs(root, themes):
    packs = []
    for theme in themes.get("themes", []):
        assets = [asset for asset in theme.get("assets", []) if asset.get("exists")]
        packs.append(
            {
                "id": f"theme-{theme['id']}",
                "type": "theme",
                "title": f"{theme['name']} Theme Pack",
                "description": theme.get("summary", ""),
                "assetCount": len(assets),
                "assets": [{"path": asset["path"], "section": asset["section"], "purpose": asset["purpose"]} for asset in assets],
                "sourcePath": theme.get("paths", {}).get("example", f"themes/{theme['id']}/example.md"),
            }
        )
    return packs


def starter_packs(recipes, bundles):
    packs = []
    for recipe in recipes.get("recipes", []):
        packs.append(
            {
                "id": f"starter-{recipe['id']}",
                "type": "starter",
                "title": f"{recipe['title']} Starter Pack",
                "description": recipe.get("summary", ""),
                "assetCount": recipe.get("assetCount", 0),
                "assets": [link for link in recipe.get("links", []) if link["path"].startswith("assets/")],
                "templateCount": recipe.get("templateCount", 0),
                "componentCount": recipe.get("componentCount", 0),
                "themeCount": recipe.get("themeCount", 0),
                "sourcePath": recipe["path"],
            }
        )
    for bundle in bundles.get("bundles", []):
        packs.append(
            {
                "id": f"bundle-{bundle['id']}",
                "type": "copy-all-bundle",
                "title": bundle["title"],
                "description": bundle.get("summary", ""),
                "assetCount": sum(1 for link in bundle.get("links", []) if link["path"].startswith("assets/")),
                "assets": [link for link in bundle.get("links", []) if link["path"].startswith("assets/")],
                "lineCount": bundle.get("lineCount", 0),
                "sourcePath": bundle["path"],
            }
        )
    return packs


def build_asset_packs(root=None):
    root = Path(root or repo_root()).resolve()
    manifest = load_json(root / "assets" / "manifest.json")
    themes = load_json(root / "themes" / "index.json")
    recipes = load_json(root / "site" / "data" / "recipes.json")
    bundles = load_json(root / "site" / "data" / "bundles.json")
    packs = category_packs(manifest) + theme_packs(root, themes) + starter_packs(recipes, bundles)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "packCount": len(packs),
        "packs": packs,
    }


def validation_errors(root, payload):
    errors = []
    for pack in payload["packs"]:
        for asset in pack.get("assets", []):
            path = asset.get("path")
            if path and path.startswith("assets/") and not (root / path).exists():
                errors.append(f"{pack['id']} references missing asset: {path}")
    return errors


def markdown_index(payload):
    lines = [
        "# Asset Packs",
        "",
        "Generated package index for static site browsing and copy workflows.",
        "",
        "| Pack | Type | Assets | Source |",
        "| --- | --- | ---: | --- |",
    ]
    for pack in payload["packs"]:
        lines.append(f"| {pack['title']} | `{pack['type']}` | {pack.get('assetCount', 0)} | `{pack.get('sourcePath', '')}` |")
    return "\n".join(lines) + "\n"


def write_asset_packs(output, markdown_output, root=None):
    root = Path(root or repo_root()).resolve()
    payload = build_asset_packs(root)
    errors = validation_errors(root, payload)
    if errors:
        raise ValueError("; ".join(errors[:10]))
    json_path = write_json(output, payload)
    markdown_output = Path(markdown_output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(markdown_index(payload), encoding="utf-8")
    return json_path, markdown_output, payload["packCount"]


def check_asset_packs(output, markdown_output, root=None):
    root = Path(root or repo_root()).resolve()
    payload = build_asset_packs(root)
    errors = validation_errors(root, payload)
    expected_json = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    expected_md = markdown_index(payload)
    failures = []
    for path, expected in [(Path(output), expected_json), (Path(markdown_output), expected_md)]:
        if not path.exists():
            failures.append((path, "missing"))
        elif path.read_text(encoding="utf-8") != expected:
            failures.append((path, "changed"))
    return failures, errors


def run_self_tests():
    payload = build_asset_packs()
    assert payload["packCount"] >= 3
    assert any(pack["type"] == "category" for pack in payload["packs"])
    assert markdown_index(payload).startswith("# Asset Packs")
    print("asset_packs.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate static asset pack metadata.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="site/data/asset-packs.json", help="Asset pack JSON path relative to repo root.")
    parser.add_argument("--markdown-output", default="site/packages/README.md", help="Asset pack Markdown index path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify asset packs are current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused packager self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    markdown_output = root / args.markdown_output
    if args.check:
        failures, errors = check_asset_packs(output, markdown_output, root)
        for path, status in failures:
            print(f"::error file={rel_path(path, root)}::Asset packs are {status}. Run npm run generate:packs.")
        for error in errors:
            print(f"::error::{error}")
        if failures or errors:
            return 1
        print("Asset packs are current.")
        return 0

    json_path, md_path, count = write_asset_packs(output, markdown_output, root)
    print(f"Wrote {count} asset pack(s) to {json_path}")
    print(f"Wrote asset pack index to {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
