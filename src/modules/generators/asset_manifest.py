from pathlib import Path
import json

try:
    from .generate_asset_previews import (
        DEFAULT_REPO_RAW_BASE,
        anchor_id,
        animation_label,
        asset_tags,
        category_units,
        clean_asset_name,
        discover_categories,
        full_preview_filename,
        parse_category_filters,
        raw_url,
        relative_asset_path,
        select_categories,
    )
    from .svg_editor_metadata import QUALITY_LEVELS, svg_editor_metadata
except ImportError:
    from generate_asset_previews import (
        DEFAULT_REPO_RAW_BASE,
        anchor_id,
        animation_label,
        asset_tags,
        category_units,
        clean_asset_name,
        discover_categories,
        full_preview_filename,
        parse_category_filters,
        raw_url,
        relative_asset_path,
        select_categories,
    )
    from svg_editor_metadata import QUALITY_LEVELS, svg_editor_metadata


ASSET_MANIFEST_SCHEMA_VERSION = 2
EDITOR_SCHEMA_VERSION = 2
GENERATOR_NAME = "src/modules/generators/generate_asset_manifest.py"
VALID_OPERATIONS = {"hideElement", "replaceColor", "replaceText", "scaleAnimationSpeed"}
SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas" / "definitions"


def preview_path(category, unit_name, asset_name):
    filename = full_preview_filename(category, unit_name)
    return f"previews/assets/{category}/{filename}#{anchor_id(asset_name)}"


def asset_record(repo_root, category, unit_name, asset_path, raw_base):
    name = clean_asset_name(asset_path)
    metadata = svg_editor_metadata(asset_path)
    label = animation_label(asset_path)
    return {
        "name": name,
        "category": category,
        "subcategory": unit_name,
        "path": relative_asset_path(repo_root, asset_path),
        "localPath": relative_asset_path(repo_root, asset_path),
        "rawUrl": raw_url(raw_base, repo_root, asset_path),
        "previewPath": preview_path(category, unit_name, name),
        "type": label,
        "animated": label == "Animated",
        "tags": asset_tags(category, unit_name, asset_path),
        "dimensions": metadata["dimensions"],
        "editorQuality": metadata["editor"]["quality"]["level"],
        "compatibilityWarnings": metadata["editor"]["warnings"],
        "editor": metadata["editor"],
    }


def build_manifest(repo_root, assets_dir, raw_base=DEFAULT_REPO_RAW_BASE, category_filters=None):
    assets_root = repo_root / assets_dir
    if not assets_root.exists():
        raise FileNotFoundError(f"Assets directory does not exist: {assets_root}")

    categories = select_categories(discover_categories(assets_root), category_filters)
    records = []
    category_counts = {}

    for category_dir in categories:
        category = category_dir.name
        category_total = 0
        for unit_name, assets in category_units(category_dir):
            unit_records = [asset_record(repo_root, category, unit_name, asset_path, raw_base) for asset_path in assets]
            records.extend(unit_records)
            category_total += len(unit_records)
        category_counts[category] = category_total

    return {
        "schemaVersion": ASSET_MANIFEST_SCHEMA_VERSION,
        "editorSchemaVersion": EDITOR_SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "assetCount": len(records),
        "categories": [category.name for category in categories],
        "categoryCounts": category_counts,
        "assets": records,
    }


def manifest_json(repo_root, assets_dir, raw_base=DEFAULT_REPO_RAW_BASE, category_filters=None):
    return json.dumps(
        build_manifest(repo_root, assets_dir, raw_base=raw_base, category_filters=category_filters),
        indent=2,
        sort_keys=True,
    ) + "\n"


def write_manifest(repo_root, assets_dir, output_file, raw_base=DEFAULT_REPO_RAW_BASE, category_filters=None):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    content = manifest_json(repo_root, assets_dir, raw_base=raw_base, category_filters=category_filters)
    output_file.write_text(content, encoding="utf-8")
    return output_file, json.loads(content)["assetCount"]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require_keys(value, keys, path, errors):
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return
    for key in keys:
        if key not in value:
            errors.append(f"{path}.{key} is required")


def validate_dimensions(value, path, errors):
    require_keys(value, {"width", "height", "viewBox", "aspectRatio"}, path, errors)
    if isinstance(value, dict) and not value.get("viewBox"):
        errors.append(f"{path}.viewBox must not be empty")


def validate_color_token(token, path, errors):
    require_keys(token, {"value", "role", "count", "attributes", "operations"}, path, errors)
    if isinstance(token, dict) and "replaceColor" not in token.get("operations", []):
        errors.append(f"{path}.operations must include replaceColor")


def validate_text_node(node, path, errors):
    require_keys(
        node,
        {"nodePath", "tag", "value", "length", "editId", "editLabel", "locked", "stable", "selector", "operations"},
        path,
        errors,
    )


def validate_removable_element(element, path, errors):
    require_keys(
        element,
        {
            "nodePath",
            "tag",
            "label",
            "editId",
            "editLabel",
            "locked",
            "stable",
            "selector",
            "operations",
            "hasText",
            "hasAnimation",
        },
        path,
        errors,
    )


def validate_warning(item, path, errors):
    require_keys(item, {"code", "severity", "message"}, path, errors)


def validate_editor_metadata(editor, path, errors):
    require_keys(
        editor,
        {
            "editable",
            "quality",
            "capabilities",
            "operations",
            "nodePathMode",
            "palette",
            "colorTokens",
            "textNodes",
            "removableElements",
            "animation",
            "warnings",
        },
        path,
        errors,
    )
    if not isinstance(editor, dict):
        return

    quality = editor.get("quality", {})
    require_keys(quality, {"level", "score", "reasons"}, f"{path}.quality", errors)
    if quality.get("level") not in QUALITY_LEVELS:
        errors.append(f"{path}.quality.level must be one of {sorted(QUALITY_LEVELS)}")

    operations = editor.get("operations", [])
    if not isinstance(operations, list):
        errors.append(f"{path}.operations must be an array")
    else:
        unknown_operations = sorted(set(operations) - VALID_OPERATIONS)
        if unknown_operations:
            errors.append(f"{path}.operations has unknown values: {', '.join(unknown_operations)}")

    for index, token in enumerate(editor.get("colorTokens", [])):
        validate_color_token(token, f"{path}.colorTokens[{index}]", errors)
    for index, node in enumerate(editor.get("textNodes", [])):
        validate_text_node(node, f"{path}.textNodes[{index}]", errors)
    for index, element in enumerate(editor.get("removableElements", [])):
        validate_removable_element(element, f"{path}.removableElements[{index}]", errors)
    for index, item in enumerate(editor.get("warnings", [])):
        validate_warning(item, f"{path}.warnings[{index}]", errors)


def validate_asset(asset, index, errors):
    path = f"assets[{index}]"
    require_keys(
        asset,
        {
            "name",
            "category",
            "subcategory",
            "path",
            "localPath",
            "rawUrl",
            "previewPath",
            "type",
            "animated",
            "tags",
            "dimensions",
            "editorQuality",
            "compatibilityWarnings",
            "editor",
        },
        path,
        errors,
    )
    if not isinstance(asset, dict):
        return
    validate_dimensions(asset.get("dimensions", {}), f"{path}.dimensions", errors)
    validate_editor_metadata(asset.get("editor", {}), f"{path}.editor", errors)
    if asset.get("editorQuality") not in QUALITY_LEVELS:
        errors.append(f"{path}.editorQuality must be one of {sorted(QUALITY_LEVELS)}")


def validate_manifest(payload):
    errors = []
    require_keys(
        payload,
        {
            "schemaVersion",
            "editorSchemaVersion",
            "generatedBy",
            "assetCount",
            "categories",
            "categoryCounts",
            "assets",
        },
        "manifest",
        errors,
    )
    if not isinstance(payload, dict):
        return errors

    if payload.get("schemaVersion") != ASSET_MANIFEST_SCHEMA_VERSION:
        errors.append(f"manifest.schemaVersion must be {ASSET_MANIFEST_SCHEMA_VERSION}")
    if payload.get("editorSchemaVersion") != EDITOR_SCHEMA_VERSION:
        errors.append(f"manifest.editorSchemaVersion must be {EDITOR_SCHEMA_VERSION}")
    assets = payload.get("assets", [])
    if not isinstance(assets, list):
        errors.append("manifest.assets must be an array")
    elif payload.get("assetCount") != len(assets):
        errors.append("manifest.assetCount must match assets length")
    for index, asset in enumerate(assets):
        validate_asset(asset, index, errors)
    return errors


def check_manifest(repo_root, assets_dir, output_file, raw_base=DEFAULT_REPO_RAW_BASE, category_filters=None):
    expected = manifest_json(repo_root, assets_dir, raw_base=raw_base, category_filters=category_filters)
    expected_errors = validate_manifest(json.loads(expected))
    if expected_errors:
        return "invalid-generated", expected_errors
    if not output_file.exists():
        return "missing", []

    actual = output_file.read_text(encoding="utf-8")
    if actual != expected:
        return "changed", []

    try:
        actual_payload = json.loads(actual)
    except json.JSONDecodeError as error:
        return "invalid-json", [str(error)]

    actual_errors = validate_manifest(actual_payload)
    if actual_errors:
        return "invalid", actual_errors
    return None, []


def print_manifest_check_failure(output_file, status, errors=None):
    rel_path = output_file.as_posix()
    print("Asset manifest is stale or invalid. Regenerate it with:")
    print()
    print(f"  python src/modules/generators/generate_asset_manifest.py --output {rel_path}")
    print()
    print(f"::error file={rel_path}::Asset manifest is {status}: {rel_path}")
    for error in (errors or [])[:20]:
        print(f"::error file={rel_path}::{error}")


def schema_paths():
    return [
        SCHEMA_DIR / "asset-manifest.schema.json",
        SCHEMA_DIR / "editor-metadata.schema.json",
    ]


def run_self_tests():
    for schema_path in schema_paths():
        assert schema_path.exists(), f"missing schema fixture: {schema_path}"
        json.loads(schema_path.read_text(encoding="utf-8"))

    repo_root = Path(__file__).resolve().parents[3]
    manifest = build_manifest(repo_root, Path("src/modules/generators"), category_filters=["fixtures"])
    assert manifest["schemaVersion"] == ASSET_MANIFEST_SCHEMA_VERSION
    assert manifest["editorSchemaVersion"] == EDITOR_SCHEMA_VERSION
    assert manifest["assetCount"] == 2
    assert validate_manifest(manifest) == []
    sample = next(asset for asset in manifest["assets"] if asset["name"] == "editor_metadata_sample")
    assert sample["editorQuality"] in QUALITY_LEVELS
    assert "replaceColor" in sample["editor"]["operations"]
    assert "previewPath" in sample
    assert sample["path"] == sample["localPath"]
    print("asset_manifest.py self-tests passed.")


__all__ = [
    "ASSET_MANIFEST_SCHEMA_VERSION",
    "EDITOR_SCHEMA_VERSION",
    "build_manifest",
    "check_manifest",
    "manifest_json",
    "parse_category_filters",
    "print_manifest_check_failure",
    "run_self_tests",
    "validate_manifest",
    "write_manifest",
]
