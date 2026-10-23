from pathlib import Path
import argparse
import copy
import json

from src.modules.common.repo import load_json, rel_path, repo_root, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/migrations/migration_registry.py"
CURRENT_MANIFEST_SCHEMA_VERSION = 2
CURRENT_EDITOR_SCHEMA_VERSION = 2


def empty_editor_metadata():
    return {
        "editable": False,
        "quality": {"level": "limited", "score": 0, "reasons": ["Migrated record needs fresh editor metadata."]},
        "capabilities": [],
        "operations": [],
        "nodePathMode": "element-child-index",
        "palette": {},
        "colorTokens": [],
        "textNodes": [],
        "removableElements": [],
        "animation": {"hasAnimation": False, "durations": [], "operations": []},
        "warnings": [{"code": "migrated-metadata", "severity": "warning", "message": "Regenerate the manifest to compute full editor metadata."}],
    }


def normalize_asset_record(asset):
    record = copy.deepcopy(asset)
    if "localPath" not in record and "path" in record:
        record["localPath"] = record["path"]
    if "animated" not in record:
        record["animated"] = record.get("type", "").lower() == "animated"
    if "previewPath" not in record and "path" in record:
        record["previewPath"] = record["path"]
    if "editorQuality" not in record:
        record["editorQuality"] = "limited"
    if "compatibilityWarnings" not in record:
        record["compatibilityWarnings"] = []
    if "editor" not in record:
        record["editor"] = empty_editor_metadata()
    if "tags" not in record:
        record["tags"] = sorted(filter(None, [record.get("category"), record.get("subcategory")]))
    return record


def manifest_v1_to_v2(payload):
    migrated = copy.deepcopy(payload)
    migrated["schemaVersion"] = CURRENT_MANIFEST_SCHEMA_VERSION
    migrated["editorSchemaVersion"] = CURRENT_EDITOR_SCHEMA_VERSION
    migrated["generatedBy"] = "src/modules/generators/generate_asset_manifest.py"
    migrated["assets"] = [normalize_asset_record(asset) for asset in migrated.get("assets", [])]
    migrated["assetCount"] = len(migrated["assets"])
    migrated["categories"] = sorted({asset.get("category", "") for asset in migrated["assets"] if asset.get("category")})
    category_counts = {}
    for asset in migrated["assets"]:
        category = asset.get("category")
        if category:
            category_counts[category] = category_counts.get(category, 0) + 1
    migrated["categoryCounts"] = dict(sorted(category_counts.items()))
    return migrated


def migrate_manifest(payload):
    version = payload.get("schemaVersion", 1)
    if version == CURRENT_MANIFEST_SCHEMA_VERSION:
        return copy.deepcopy(payload), []
    if version == 1:
        return manifest_v1_to_v2(payload), ["manifest-v1-to-v2"]
    raise ValueError(f"Unsupported manifest schema version: {version}")


def migration_plan(root=None):
    root = Path(root or repo_root()).resolve()
    manifest_path = root / "assets" / "manifest.json"
    current_manifest = load_json(manifest_path) if manifest_path.exists() else {}
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "current": {
            "assetManifestSchemaVersion": CURRENT_MANIFEST_SCHEMA_VERSION,
            "editorSchemaVersion": CURRENT_EDITOR_SCHEMA_VERSION,
            "repositoryManifestVersion": current_manifest.get("schemaVersion"),
        },
        "migrations": [
            {
                "id": "manifest-v1-to-v2",
                "from": {"assetManifestSchemaVersion": 1},
                "to": {"assetManifestSchemaVersion": 2, "editorSchemaVersion": 2},
                "changes": [
                    "Backfill localPath from path.",
                    "Backfill animated from type.",
                    "Backfill previewPath when missing.",
                    "Add empty editor metadata as a temporary migration bridge.",
                    "Recompute categoryCounts and assetCount.",
                ],
                "followUp": "Regenerate assets/manifest.json for complete editor metadata after migrating.",
            }
        ],
    }


def write_plan(output, root=None):
    payload = migration_plan(root)
    return write_json(output, payload), len(payload["migrations"])


def check_plan(output, root=None):
    payload = migration_plan(root)
    expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = Path(output)
    status = None
    if not output.exists():
        status = "missing"
    elif output.read_text(encoding="utf-8") != expected:
        status = "changed"
    errors = []
    current = payload["current"].get("repositoryManifestVersion")
    if current and current != CURRENT_MANIFEST_SCHEMA_VERSION:
        errors.append(f"assets/manifest.json is schemaVersion {current}; expected {CURRENT_MANIFEST_SCHEMA_VERSION}.")
    return status, errors


def run_self_tests():
    legacy = {
        "schemaVersion": 1,
        "assets": [
            {
                "name": "Demo",
                "category": "icons",
                "subcategory": "core",
                "path": "assets/icons/core/demo.svg",
                "rawUrl": "https://example.com/demo.svg",
                "type": "Static",
            }
        ],
    }
    migrated, steps = migrate_manifest(legacy)
    assert steps == ["manifest-v1-to-v2"]
    assert migrated["schemaVersion"] == CURRENT_MANIFEST_SCHEMA_VERSION
    assert migrated["assets"][0]["localPath"] == legacy["assets"][0]["path"]
    assert migrated["assets"][0]["editor"]["quality"]["level"] == "limited"
    print("migration_registry.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate migration metadata and migrate legacy generated data.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--plan-output", default="site/data/migration-plan.json", help="Migration plan path relative to repo root.")
    parser.add_argument("--input", help="Input manifest JSON to migrate.")
    parser.add_argument("--output", help="Output path for migrated manifest JSON.")
    parser.add_argument("--check", action="store_true", help="Verify migration plan is current without writing.")
    parser.add_argument("--dry-run", action="store_true", help="Print migration steps without writing output.")
    parser.add_argument("--self-test", action="store_true", help="Run focused migration self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    plan_output = root / args.plan_output
    if args.check:
        status, errors = check_plan(plan_output, root)
        if status:
            print(f"::error file={rel_path(plan_output, root)}::Migration plan is {status}. Run npm run generate:migrations.")
        for error in errors:
            print(f"::error::{error}")
        if status or errors:
            return 1
        print("Migration plan is current.")
        return 0

    if args.input:
        payload = load_json(args.input)
        migrated, steps = migrate_manifest(payload)
        print(json.dumps({"steps": steps, "schemaVersion": migrated.get("schemaVersion")}, indent=2, sort_keys=True))
        if not args.dry_run:
            if not args.output:
                parser.error("--output is required when migrating without --dry-run.")
            write_json(args.output, migrated)
        return 0

    path, count = write_plan(plan_output, root)
    print(f"Wrote {count} migration record(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
