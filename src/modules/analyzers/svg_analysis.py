from pathlib import Path
import argparse
import json
import xml.etree.ElementTree as ET

from src.modules.common.repo import load_json, rel_path, repo_root, write_json
from src.modules.generators.svg_editor_metadata import (
    CSS_DECLARATION_RE,
    colors_from_value,
    hex_to_rgb,
    local_name,
    parse_number,
    parse_view_box,
)


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/analyzers/svg_analysis.py"
LARGE_SVG_BYTES = 50_000
VERY_COMPLEX_ELEMENTS = 120
HIGH_MOTION_ANIMATIONS = 8


def relative_luminance(color):
    rgb = hex_to_rgb(color)
    if not rgb:
        return None

    channels = []
    for channel in rgb:
        value = channel / 255
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(foreground, background):
    fg = relative_luminance(foreground)
    bg = relative_luminance(background)
    if fg is None or bg is None:
        return None
    light = max(fg, bg)
    dark = min(fg, bg)
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
    aria_labelledby = root.attrib.get("aria-labelledby")
    title_count = sum(1 for element in root.iter() if local_name(element.tag) == "title")
    desc_count = sum(1 for element in root.iter() if local_name(element.tag) == "desc")
    if role != "img":
        flags.append("missing-img-role")
    if not aria_label and not aria_labelledby and title_count == 0:
        flags.append("missing-accessible-label")
    if desc_count == 0:
        flags.append("missing-desc")
    return flags


def style_property(element, property_name):
    for declaration in CSS_DECLARATION_RE.finditer(element.attrib.get("style", "")):
        if declaration.group("property").lower() == property_name.lower():
            return declaration.group("value").strip()
    return None


def first_literal_color(value):
    colors = colors_from_value(value)
    return colors[0] if colors else None


def inherited_color(element, parent_map, property_name="fill"):
    current = element
    while current is not None:
        value = style_property(current, property_name) or current.attrib.get(property_name)
        color = first_literal_color(value)
        if color:
            return color
        current = parent_map.get(current)
    return None


def effective_opacity(element, parent_map):
    opacity = 1.0
    current = element
    while current is not None:
        value = style_property(current, "opacity") or current.attrib.get("opacity")
        if value is not None:
            try:
                opacity *= float(value)
            except ValueError:
                return None
        current = parent_map.get(current)
    return opacity


def element_point(element, parent_map):
    current = element
    while current is not None and local_name(current.tag) in {"text", "tspan", "textPath"}:
        x = parse_number(current.attrib.get("x"))
        y = parse_number(current.attrib.get("y"))
        if x is not None and y is not None:
            return float(x), float(y)
        current = parent_map.get(current)
    return None


def rect_contains(rect, point):
    x = parse_number(rect.attrib.get("x")) or 0
    y = parse_number(rect.attrib.get("y")) or 0
    width = parse_number(rect.attrib.get("width"))
    height = parse_number(rect.attrib.get("height"))
    if width is None or height is None:
        return False
    return x <= point[0] <= x + width and y <= point[1] <= y + height


def sibling_background(element, parent_map):
    point = element_point(element, parent_map)
    if point is None:
        return None

    parent = parent_map.get(element)
    current = element
    while parent is not None and local_name(parent.tag) in {"text", "tspan"}:
        current = parent
        parent = parent_map.get(parent)
    if parent is None:
        return None

    siblings = list(parent)
    index = next((position for position, sibling in enumerate(siblings) if sibling is current), None)
    if index is None:
        return None
    for sibling in reversed(siblings[:index]):
        if local_name(sibling.tag) != "rect" or not rect_contains(sibling, point):
            continue
        opacity = effective_opacity(sibling, parent_map)
        if opacity is None or opacity < 1:
            continue
        color = inherited_color(sibling, parent_map)
        if color:
            return color
    return None


def canvas_background(root, parent_map):
    style_background = style_property(root, "background-color") or style_property(root, "background")
    color = first_literal_color(style_background)
    if color:
        return color

    view_box = parse_view_box(root.attrib.get("viewBox") or root.attrib.get("viewbox"))
    if not view_box:
        return None
    min_x, min_y, width, height = [float(value) for value in view_box]
    for element in root.iter():
        if local_name(element.tag) != "rect":
            continue
        rect_x = parse_number(element.attrib.get("x")) or 0
        rect_y = parse_number(element.attrib.get("y")) or 0
        rect_width = parse_number(element.attrib.get("width"))
        rect_height = parse_number(element.attrib.get("height"))
        if rect_width is None or rect_height is None:
            continue
        covers_canvas = (
            rect_x <= min_x
            and rect_y <= min_y
            and rect_width >= width * 0.8
            and rect_height >= height * 0.8
        )
        if covers_canvas:
            color = inherited_color(element, parent_map)
            if color:
                return color
    return None


def contrast_flags(root):
    flags = []
    seen = set()
    parent_map = {child: parent for parent in root.iter() for child in parent}
    fallback_background = canvas_background(root, parent_map)
    for element in root.iter():
        if local_name(element.tag) not in {"text", "tspan", "textPath"}:
            continue
        text_color = inherited_color(element, parent_map)
        background = sibling_background(element, parent_map) or fallback_background
        if not text_color or not background or text_color == background:
            continue
        pair = (text_color, background)
        if pair in seen:
            continue
        seen.add(pair)
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

    contrast = contrast_flags(root) if parse_error is None else []
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
    assert contrast_ratio("#000000", "#ffffff") == 21.0
    icon = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><circle fill="#777777" cx="5" cy="5" r="4"/></svg>')
    assert contrast_flags(icon) == []
    readable = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><rect width="100" height="50" fill="#ffffff"/><text x="10" y="25" fill="#111111">Readable</text></svg>')
    assert contrast_flags(readable) == []
    low_contrast = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><rect width="100" height="50" fill="#777777"/><text x="10" y="25" fill="#888888">Faint</text></svg>')
    assert contrast_flags(low_contrast)[0]["ratio"] < 4.5
    translucent_accent = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><rect width="100" height="50" fill="#111827"/><rect width="100" height="50" fill="#22d3ee" opacity=".12"/><text x="10" y="25" fill="#cbd5e1">Readable</text></svg>')
    assert contrast_flags(translucent_accent) == []

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
