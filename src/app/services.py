from pathlib import Path
import argparse
import json
import re
import subprocess

from src.modules.common.repo import load_json, rel_path, repo_root
from src.modules.editor.svg_editor import apply_operations
from src.modules.renderers.svg_to_gif import (
    DEFAULT_BACKGROUND,
    DEFAULT_DURATION_MS,
    DEFAULT_FPS,
    DEFAULT_MAX_HEIGHT,
    DEFAULT_MAX_WIDTH,
    DEFAULT_MIN_HEIGHT,
    DEFAULT_MIN_WIDTH,
    html_image,
    markdown_image,
    render_svg_markup_to_gif,
)
from src.modules.reports.quality_report import build_quality_report


SAFE_FILE_RE = re.compile(r"[^A-Za-z0-9._-]+")

DATA_FILES = {
    "assets": "site/data/assets.json",
    "manifest": "assets/manifest.json",
    "analysis": "site/data/svg-analysis.json",
    "search": "site/data/search-index.json",
    "templates": "site/data/templates.json",
    "components": "site/data/components.json",
    "tags": "site/data/tag-index.json",
    "themes": "site/data/themes.json",
    "recipes": "site/data/recipes.json",
    "bundles": "site/data/bundles.json",
    "editor-presets": "site/data/editor-presets.json",
    "editor-capabilities": "site/data/editor-capabilities.json",
    "theme-palettes": "site/data/theme-palettes.json",
    "compatibility": "site/data/compatibility-report.json",
    "packs": "site/data/asset-packs.json",
    "quality": "site/data/quality-report.json",
    "migrations": "site/data/migration-plan.json",
    "schemas": "site/data/schema-catalog.json",
    "provenance": "assets/provenance.json",
    "render-smoke": "site/data/svg-render-smoke.json",
}

COMMANDS = {
    "generate-all-data": ["npm", "run", "generate:all-data"],
    "generate-previews": ["npm", "run", "generate:previews"],
    "check-all": ["npm", "run", "check:all"],
    "modules-check": ["npm", "run", "modules:check"],
    "modules-report": ["npm", "run", "modules:report"],
    "optimize-svg": ["npm", "run", "optimize:svg"],
}


def root_path(root=None):
    return Path(root or repo_root()).resolve()


def ensure_within(path, parent):
    path = Path(path).resolve()
    parent = Path(parent).resolve()
    path.relative_to(parent)
    return path


def safe_asset_path(asset_path, root=None):
    root = root_path(root)
    normalized = asset_path.replace("\\", "/").lstrip("/")
    if normalized == "assets":
        raise ValueError("Provide a concrete SVG path under assets/.")
    if normalized.startswith("assets/"):
        normalized = normalized[len("assets/") :]
    path = ensure_within(root / "assets" / normalized, root / "assets")
    if path.suffix.lower() != ".svg":
        raise ValueError("Only SVG assets can be read through the local studio.")
    if not path.exists():
        raise FileNotFoundError(normalized)
    return path


def safe_output_dir(output_dir, root=None):
    root = root_path(root)
    raw = str(output_dir or "output/gifs").strip().replace("\\", "/")
    if not raw:
        raw = "output/gifs"
    target = Path(raw)
    if target.is_absolute():
        resolved = ensure_within(target, root)
    else:
        resolved = ensure_within(root / raw.lstrip("/"), root)
    relative = rel_path(resolved, root)
    if relative in {"", "."} or relative == ".git" or relative.startswith(".git/"):
        raise ValueError("Choose an output folder inside the repository and outside .git/.")
    return resolved, relative


def safe_gif_file_name(file_name, fallback="readme-ux-export.gif"):
    raw = Path(str(file_name or fallback).strip()).name
    stem = Path(raw).stem or Path(fallback).stem
    safe_stem = SAFE_FILE_RE.sub("-", stem).strip("._-").lower()
    if not safe_stem:
        safe_stem = "readme-ux-export"
    return f"{safe_stem}.gif"


def safe_repo_gif_path(gif_path, root=None):
    root = root_path(root)
    raw = str(gif_path or "").strip().replace("\\", "/").lstrip("/")
    if not raw:
        raise ValueError("Provide a GIF path.")
    path = ensure_within(root / raw, root)
    if path.suffix.lower() != ".gif":
        raise ValueError("Only GIF files can be served through this route.")
    if not path.exists():
        raise FileNotFoundError(raw)
    return path


def bounded_int(payload, key, default, minimum, maximum):
    value = payload.get(key, default)
    try:
        value = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{key} must be an integer.") from error
    if value < minimum or value > maximum:
        raise ValueError(f"{key} must be between {minimum} and {maximum}.")
    return value


def normalized_background(value):
    value = str(value or DEFAULT_BACKGROUND).strip()
    if value == "transparent":
        return value
    if re.fullmatch(r"#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?(?:[0-9A-Fa-f]{2})?", value):
        return value
    if re.fullmatch(r"[A-Za-z]+", value):
        return value.lower()
    raise ValueError("background must be a hex color, named color, or transparent.")


def load_data(name, root=None):
    root = root_path(root)
    if name not in DATA_FILES:
        raise KeyError(f"Unknown data file: {name}")
    path = root / DATA_FILES[name]
    if not path.exists():
        raise FileNotFoundError(DATA_FILES[name])
    return load_json(path)


def manifest(root=None):
    try:
        return load_data("manifest", root)
    except FileNotFoundError:
        return load_data("assets", root)


def list_assets(root=None, query="", category="", subcategory="", tag="", animated=None, editor_quality="", limit=240):
    payload = manifest(root)
    assets = payload.get("assets", [])
    query = (query or "").strip().lower()
    category = (category or "").strip().lower()
    subcategory = (subcategory or "").strip().lower()
    tag = (tag or "").strip().lower()
    editor_quality = (editor_quality or "").strip().lower()

    filtered = []
    for asset in assets:
        tags = [item.lower() for item in asset.get("tags", [])]
        haystack = " ".join([asset.get("name", ""), asset.get("localPath", ""), asset.get("category", ""), asset.get("subcategory", ""), " ".join(tags)]).lower()
        if query and query not in haystack:
            continue
        if category and asset.get("category", "").lower() != category:
            continue
        if subcategory and asset.get("subcategory", "").lower() != subcategory:
            continue
        if tag and tag not in tags:
            continue
        if animated is not None and bool(asset.get("animated")) != bool(animated):
            continue
        if editor_quality and asset.get("editorQuality", "").lower() != editor_quality:
            continue
        filtered.append(asset)
        if limit and len(filtered) >= limit:
            break

    return {
        "assetCount": payload.get("assetCount", len(assets)),
        "matchCount": len(filtered),
        "categories": payload.get("categories", sorted({asset.get("category") for asset in assets if asset.get("category")})),
        "categoryCounts": payload.get("categoryCounts", {}),
        "assets": filtered,
    }


def asset_detail(asset_path, root=None):
    root = root_path(root)
    path = safe_asset_path(asset_path, root)
    relative = rel_path(path, root)
    records = [asset for asset in manifest(root).get("assets", []) if asset.get("localPath") == relative or asset.get("path") == relative]
    return {
        "asset": records[0] if records else {"name": path.stem, "localPath": relative},
        "source": path.read_text(encoding="utf-8"),
    }


def edit_svg(payload, root=None):
    root = root_path(root)
    if payload.get("source"):
        source = payload["source"]
        source_path = None
    elif payload.get("path"):
        detail = asset_detail(payload["path"], root)
        source = detail["source"]
        source_path = detail["asset"].get("localPath")
    else:
        raise ValueError("Provide either `path` or `source`.")

    edited, summary = apply_operations(source, payload.get("operations", {}))
    return {
        "sourcePath": source_path,
        "summary": summary,
        "svg": edited,
        "byteLength": len(edited.encode("utf-8")),
    }


def gif_export_source(payload, root=None):
    root = root_path(root)
    if payload.get("source"):
        source = str(payload["source"])
        if not source.strip():
            raise ValueError("source cannot be empty.")
        source_path = payload.get("sourcePath")
        fallback_label = Path(source_path or "custom-svg").stem
        return source, source_path, payload.get("name") or fallback_label

    if payload.get("path"):
        detail = asset_detail(payload["path"], root)
        return detail["source"], detail["asset"].get("localPath"), detail["asset"].get("name") or Path(payload["path"]).stem

    raise ValueError("Provide either `path` or `source`.")


def export_gif(payload, root=None):
    root = root_path(root)
    source, source_path, label = gif_export_source(payload, root)
    output_dir, output_dir_relative = safe_output_dir(payload.get("outputDir"), root)
    fallback_name = f"{Path(source_path or label or 'readme-ux-export').stem}.gif"
    output_path = ensure_within(output_dir / safe_gif_file_name(payload.get("fileName"), fallback_name), output_dir)
    duration_ms = bounded_int(payload, "durationMs", DEFAULT_DURATION_MS, 100, 10000)
    fps = bounded_int(payload, "fps", DEFAULT_FPS, 1, 30)
    max_width = bounded_int(payload, "maxWidth", DEFAULT_MAX_WIDTH, 64, 1920)
    max_height = bounded_int(payload, "maxHeight", DEFAULT_MAX_HEIGHT, 64, 1080)
    min_width = bounded_int(payload, "minWidth", DEFAULT_MIN_WIDTH, 24, 1920)
    min_height = bounded_int(payload, "minHeight", DEFAULT_MIN_HEIGHT, 24, 1080)
    background = normalized_background(payload.get("background"))

    if min_width > max_width:
        raise ValueError("minWidth cannot be larger than maxWidth.")
    if min_height > max_height:
        raise ValueError("minHeight cannot be larger than maxHeight.")

    metadata = render_svg_markup_to_gif(
        source,
        output_path,
        duration_ms=duration_ms,
        fps=fps,
        max_width=max_width,
        max_height=max_height,
        min_width=min_width,
        min_height=min_height,
        background=background,
    )
    output_relative = rel_path(output_path, root)
    copy_label = str(label or output_path.stem).strip() or output_path.stem
    return {
        "ok": True,
        "sourcePath": source_path,
        "outputDir": output_dir_relative,
        "outputPath": output_relative,
        "absolutePath": str(output_path),
        "byteLength": output_path.stat().st_size,
        "dimensions": metadata["dimensions"],
        "renderSettings": metadata["renderSettings"],
        "copy": {
            "markdown": markdown_image(copy_label, output_relative),
            "html": html_image(copy_label, output_relative),
        },
    }


def repository_summary(root=None):
    root = root_path(root)
    manifest_payload = manifest(root)
    quality = build_quality_report(root)
    data_files = [
        {"name": name, "path": path, "exists": (root / path).exists()}
        for name, path in sorted(DATA_FILES.items())
    ]
    return {
        "name": "readme-ux-kit local studio",
        "localOnly": True,
        "assetCount": manifest_payload.get("assetCount", len(manifest_payload.get("assets", []))),
        "categoryCounts": manifest_payload.get("categoryCounts", {}),
        "qualitySummary": quality.get("summary", {}),
        "dataFiles": data_files,
        "commands": sorted(COMMANDS),
    }


def run_command(name, root=None, timeout=300):
    root = root_path(root)
    if name not in COMMANDS:
        raise KeyError(f"Unknown command: {name}")
    result = subprocess.run(
        COMMANDS[name],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return {
        "command": name,
        "args": COMMANDS[name],
        "returnCode": result.returncode,
        "ok": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def run_self_tests():
    assert "check-all" in COMMANDS
    assert "assets" in DATA_FILES
    assert safe_output_dir("output/gifs")[1] == "output/gifs"
    assert safe_gif_file_name("../Demo GIF.svg", "fallback.gif") == "demo-gif.gif"
    try:
        safe_output_dir(".git/hooks")
        raise AssertionError(".git output path should be rejected")
    except ValueError:
        pass
    sample = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40" role="img" aria-label="Demo">'
        '<title>Demo</title><text id="title" fill="#2563eb">Demo</text></svg>'
    )
    edited = edit_svg({"source": sample, "operations": {"replaceColors": {"#2563eb": "#0f766e"}, "replaceText": [{"target": "title", "to": "Local Studio"}]}})
    assert "#0f766e" in edited["svg"]
    assert "Local Studio" in edited["svg"]
    if (root_path() / "assets" / "manifest.json").exists():
        assert list_assets(limit=1)["assetCount"] >= 1
    print("src.app.services self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Local studio service helpers.")
    parser.add_argument("--self-test", action="store_true", help="Run service self-tests and exit.")
    args = parser.parse_args()
    if args.self_test:
        run_self_tests()
        return 0
    print(json.dumps(repository_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
