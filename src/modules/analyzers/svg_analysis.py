from pathlib import Path
import argparse
import json
import xml.etree.ElementTree as ET

from src.modules.common.repo import load_json, rel_path, repo_root, write_json
from src.modules.generators.svg_editor_metadata import color_stats, local_name


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/analyzers/svg_analysis.py"
LARGE_SVG_BYTES = 50_000
VERY_COMPLEX_ELEMENTS = 120
HIGH_MOTION_ANIMATIONS = 8


def contrast_ratio(foreground, background):
    fg = color_stats(foreground)
    bg = color_stats(background)
    if not fg or not bg:
        return None
    light = max(fg["luminance"], bg["luminance"])
    dark = min(fg["luminance"], bg["luminance"])
    return round((light + 0.05) / (dark + 0.05), 2)


def parse_svg(path):
    return ET.fromstring(path.read_text(encoding="utf-8"))


def tag_counts(root):
    counts = {}
    for element in root.iter():
        name = local_name(element.tag)
        if not name:
            continue
        counts[name] = counts.get(name, 0) + 1
    return counts


def accessibility_flags(root):
    flags = []
    role = root.attrib.get("role")
    aria_label = root.attrib.get("aria-label")
    title_count = sum(1 for element in root.iter() if local_name(element.tag) == "title")
    desc_count = sum(1 for element in root.iter() if local_name(element.tag) == "desc")
    if role != "img":
        flags.append("missing-img-role")
    if not aria_label and title_count == 0:
        flags.append("missing-accessible-label")
    if desc_count == 0:
        flags.append("missing-desc")
    return flags


def color_lookup(editor, role):
    return editor.get("palette", {}).get(role, [])


def contrast_flags(editor):
    flags = []
    backgrounds = color_lookup(editor, "background") + color_lookup(editor, "surface")
    texts = color_lookup(editor, "text") + color_lookup(editor, "mutedText")
    for text_color in texts[:3]:
        for background in backgrounds[:3]:
            ratio = contrast_ratio(text_color, background)
            if ratio is not None and ratio < 4.5:
                flags.append(
                    {
                        "text": text_color,
                        "background": background,
                        "ratio": ratio,
                        "threshold": 4.5,
                    }
                )
    return flags


def complexity_score(counts, file_size):
    score = counts.get("path", 0) * 2
    score += counts.get("linearGradient", 0) * 4 + counts.get("radialGradient", 0) * 4
    score += counts.get("filter", 0) * 8 + counts.get("mask", 0) * 8 + counts.get("clipPath", 0) * 5
    score += sum(counts.values())
    score += file_size // 2500
    return int(score)


def motion_score(counts, editor):
    return int((counts.get("animate", 0) + counts.get("animateTransform", 0) + counts.get("animateMotion", 0)) * 2 + len(editor.get("animation", {}).get("durations", [])))


def analyze_asset(root_dir, asset):
    path = root_dir / asset["localPath"]
    file_size = path.stat().st_size
    try:
        root = parse_svg(path)
        counts = tag_counts(root)
        parse_error = None
    except ET.ParseError as error:
        counts = {}
        parse_error = str(error)

    editor = asset.get("editor", {})
    complexity = complexity_score(counts, file_size)
    motion = motion_score(counts, editor)
    duplicate_colors = [token["value"] for token in editor.get("colorTokens", []) if token.get("count", 0) >= 10]
    flags = []
    if parse_error:
        flags.append("invalid-svg")
    if file_size >= LARGE_SVG_BYTES:
        flags.append("large-file")
    if sum(counts.values()) >= VERY_COMPLEX_ELEMENTS:
        flags.append("very-complex")
    if motion >= HIGH_MOTION_ANIMATIONS:
        flags.append("high-motion")
    if duplicate_colors:
        flags.append("duplicate-heavy-palette")

    access_flags = accessibility_flags(root) if parse_error is None else ["invalid-svg"]
    if access_flags:
        flags.append("accessibility-risk")

    contrast = contrast_flags(editor)
    if contrast:
        flags.append("contrast-risk")

    return {
        "name": asset["name"],
        "path": asset["localPath"],
        "category": asset["category"],
        "subcategory": asset["subcategory"],
        "fileSize": file_size,
        "elementCount": sum(counts.values()),
        "tagCounts": counts,
        "complexityScore": complexity,
        "motionScore": motion,
        "colorCount": len(editor.get("colorTokens", [])),
        "duplicateColors": duplicate_colors,
        "accessibilityFlags": access_flags,
        "contrastFlags": contrast,
        "flags": sorted(set(flags)),
    }


def build_analysis(root_dir=None, manifest_path=None):
    root_dir = Path(root_dir or repo_root()).resolve()
    manifest_path = Path(manifest_path or root_dir / "assets" / "manifest.json")
    manifest = load_json(manifest_path)
    assets = [analyze_asset(root_dir, asset) for asset in manifest["assets"]]
    category_counts = {}
    flag_counts = {}
    for asset in assets:
        category_counts[asset["category"]] = category_counts.get(asset["category"], 0) + 1
        for flag in asset["flags"]:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1

    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "assetCount": len(assets),
        "summary": {
            "categoryCounts": dict(sorted(category_counts.items())),
            "flagCounts": dict(sorted(flag_counts.items())),
            "largestAssets": sorted(assets, key=lambda item: item["fileSize"], reverse=True)[:20],
            "mostComplexAssets": sorted(assets, key=lambda item: item["complexityScore"], reverse=True)[:20],
            "highestMotionAssets": sorted(assets, key=lambda item: item["motionScore"], reverse=True)[:20],
        },
        "assets": sorted(assets, key=lambda item: item["path"]),
    }


def write_analysis(output, root_dir=None, manifest_path=None):
    payload = build_analysis(root_dir=root_dir, manifest_path=manifest_path)
    return write_json(output, payload), payload["assetCount"]


def check_analysis(output, root_dir=None, manifest_path=None):
    expected = json.dumps(build_analysis(root_dir=root_dir, manifest_path=manifest_path), indent=2, sort_keys=True) + "\n"
    output = Path(output)
    if not output.exists():
        return "missing"
    if output.read_text(encoding="utf-8") != expected:
        return "changed"
    return None


def run_self_tests():
    root = repo_root()
    manifest = root / "assets" / "manifest.json"
    if manifest.exists():
        payload = build_analysis(root, manifest)
        assert payload["assetCount"] > 0
        first = payload["assets"][0]
        assert "complexityScore" in first
        assert "motionScore" in first
        assert "accessibilityFlags" in first
    print("svg_analysis.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Analyze SVG assets for complexity, motion, palette, size, and accessibility signals.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--manifest", default="assets/manifest.json", help="Manifest path relative to repo root.")
    parser.add_argument("--output", default="site/data/svg-analysis.json", help="Output report path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify the analysis report is current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run analyzer self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    manifest = root / args.manifest
    if args.check:
        status = check_analysis(output, root, manifest)
        if status:
            print(f"::error file={rel_path(output, root)}::SVG analysis report is {status}. Run npm run generate:analysis.")
            return 1
        print("SVG analysis report is current.")
        return 0

    path, count = write_analysis(output, root, manifest)
    print(f"Wrote SVG analysis for {count} asset(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
