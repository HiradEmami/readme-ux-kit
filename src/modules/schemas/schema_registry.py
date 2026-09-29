from pathlib import Path
import argparse
import json

from src.modules.common.repo import load_json, rel_path, repo_root, write_json
from src.modules.generators.asset_manifest import validate_manifest


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/schemas/schema_registry.py"
SCHEMA_DIR = Path(__file__).resolve().parent / "definitions"
GENERATED_DATA_FILES = (
    "assets/manifest.json",
    "assets/provenance.json",
    "components/index.json",
    "templates/index.json",
    "themes/index.json",
    "site/data/assets.json",
    "site/data/editor-presets.json",
    "site/data/theme-palettes.json",
    "site/data/editor-capabilities.json",
    "site/data/svg-analysis.json",
    "site/data/search-index.json",
    "site/data/templates.json",
    "site/data/components.json",
    "site/data/tag-index.json",
    "site/data/markdown-snippets.json",
    "site/data/themes.json",
    "site/data/recipes.json",
    "site/data/bundles.json",
    "site/data/svg-render-smoke.json",
    "site/data/compatibility-report.json",
    "site/data/asset-packs.json",
    "site/data/quality-report.json",
    "site/data/migration-plan.json",
)
COUNT_KEYS = {
    "assetCount": "assets",
    "themeCount": "themes",
    "templateCount": "templates",
    "componentCount": "components",
    "recipeCount": "recipes",
    "bundleCount": "bundles",
    "snippetCount": "snippets",
    "operationCount": "operations",
    "packCount": "packs",
}


def schema_files():
    return sorted(SCHEMA_DIR.glob("*.schema.json"), key=lambda path: path.name)


def schema_catalog(root=None):
    root = Path(root or repo_root()).resolve()
    schemas = []
    for path in schema_files():
        payload = load_json(path)
        schemas.append(
            {
                "id": payload.get("$id", path.name),
                "title": payload.get("title", path.stem),
                "path": rel_path(path, root),
                "draft": payload.get("$schema", ""),
            }
        )
    data_files = [{"path": name, "exists": (root / name).exists()} for name in GENERATED_DATA_FILES]
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "schemaCount": len(schemas),
        "schemas": schemas,
        "dataFiles": data_files,
    }


def validate_schema_definitions(root=None):
    root = Path(root or repo_root()).resolve()
    errors = []
    for path in schema_files():
        try:
            payload = load_json(path)
        except json.JSONDecodeError as error:
            errors.append(f"{rel_path(path, root)} is invalid JSON: {error}")
            continue
        for key in ["$schema", "$id", "title", "type"]:
            if key not in payload:
                errors.append(f"{rel_path(path, root)} is missing {key}.")
    return errors


def validate_count_fields(path, payload):
    errors = []
    for count_key, list_key in COUNT_KEYS.items():
        if count_key in payload and list_key in payload and isinstance(payload[list_key], list):
            if payload[count_key] != len(payload[list_key]):
                errors.append(f"{path}: {count_key} does not match {list_key} length.")
    return errors


def validate_generated_data(root=None):
    root = Path(root or repo_root()).resolve()
    errors = []
    for name in GENERATED_DATA_FILES:
        path = root / name
        if not path.exists():
            errors.append(f"{name} is missing.")
            continue
        try:
            payload = load_json(path)
        except json.JSONDecodeError as error:
            errors.append(f"{name} is invalid JSON: {error}")
            continue
        if "schemaVersion" not in payload:
            errors.append(f"{name} is missing schemaVersion.")
        if name.endswith("manifest.json"):
            errors.extend(f"{name}: {error}" for error in validate_manifest(payload))
        errors.extend(validate_count_fields(name, payload))
    return errors


def write_catalog(output, root=None):
    payload = schema_catalog(root)
    return write_json(output, payload), payload["schemaCount"]


def check_catalog(output, root=None):
    payload = schema_catalog(root)
    expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = Path(output)
    status = None
    if not output.exists():
        status = "missing"
    elif output.read_text(encoding="utf-8") != expected:
        status = "changed"
    return status, validate_schema_definitions(root) + validate_generated_data(root)


def run_self_tests():
    schemas = schema_files()
    assert schemas
    assert validate_schema_definitions() == []
    sample = {"schemaVersion": 1, "assetCount": 1, "assets": [{}, {}]}
    assert validate_count_fields("sample.json", sample)
    print("schema_registry.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate a schema catalog and validate generated repository data.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="site/data/schema-catalog.json", help="Schema catalog path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify the schema catalog and generated data without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused schema self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    if args.check:
        status, errors = check_catalog(output, root)
        if status:
            print(f"::error file={rel_path(output, root)}::Schema catalog is {status}. Run npm run generate:schemas.")
        for error in errors:
            print(f"::error::{error}")
        if status or errors:
            return 1
        print("Schema catalog and generated data are current.")
        return 0

    path, count = write_catalog(output, root)
    print(f"Wrote {count} schema record(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
