from pathlib import Path
import argparse
import html
import importlib.util
import json
import shutil
import xml.etree.ElementTree as ET

from src.modules.common.repo import load_json, rel_path, repo_root, write_json
from src.modules.generators.svg_editor_metadata import local_name


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/renderers/svg_smoke_render.py"
VISUAL_TAGS = {
    "circle",
    "ellipse",
    "image",
    "line",
    "path",
    "polygon",
    "polyline",
    "rect",
    "text",
    "use",
}


def renderer_backend():
    if importlib.util.find_spec("cairosvg") is not None:
        return "cairosvg"
    for executable in ["rsvg-convert", "magick"]:
        if shutil.which(executable):
            return executable
    return None


def parse_svg(path):
    return ET.fromstring(path.read_text(encoding="utf-8"))


def viewbox_status(root):
    viewbox = root.attrib.get("viewBox")
    if not viewbox:
        return {"hasViewBox": False, "width": root.attrib.get("width"), "height": root.attrib.get("height"), "risk": "missing-viewbox"}
    parts = viewbox.replace(",", " ").split()
    if len(parts) != 4:
        return {"hasViewBox": True, "viewBox": viewbox, "risk": "invalid-viewbox"}
    try:
        values = [float(part) for part in parts]
    except ValueError:
        return {"hasViewBox": True, "viewBox": viewbox, "risk": "invalid-viewbox"}
    risk = None if values[2] > 0 and values[3] > 0 else "nonpositive-viewbox"
    return {"hasViewBox": True, "viewBox": viewbox, "width": values[2], "height": values[3], "risk": risk}


def smoke_asset(root_dir, asset):
    path = root_dir / asset["localPath"]
    flags = []
    try:
        svg_root = parse_svg(path)
        visual_count = sum(1 for element in svg_root.iter() if local_name(element.tag) in VISUAL_TAGS)
        status = viewbox_status(svg_root)
        if visual_count == 0:
            flags.append("blank-risk")
        if status.get("risk"):
            flags.append(status["risk"])
        parse_error = None
    except ET.ParseError as error:
        visual_count = 0
        status = {"risk": "invalid-svg"}
        parse_error = str(error)
        flags.append("invalid-svg")
    return {
        "name": asset["name"],
        "path": asset["localPath"],
        "category": asset["category"],
        "subcategory": asset["subcategory"],
        "previewPath": asset.get("previewPath"),
        "visualElementCount": visual_count,
        "viewBox": status,
        "parseError": parse_error,
        "flags": sorted(set(flags)),
    }


def build_smoke_report(root=None, manifest_path=None, contact_sheet_path="site/svg-contact-sheet.html"):
    root = Path(root or repo_root()).resolve()
    manifest = load_json(manifest_path or root / "assets" / "manifest.json")
    assets = [smoke_asset(root, asset) for asset in manifest["assets"]]
    flag_counts = {}
    for asset in assets:
        for flag in asset["flags"]:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1
    backend = renderer_backend()
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "renderMode": "png-capable" if backend else "metadata-smoke",
        "rendererBackend": backend,
        "contactSheetPath": contact_sheet_path,
        "assetCount": len(assets),
        "summary": {"flagCounts": dict(sorted(flag_counts.items()))},
        "assets": sorted(assets, key=lambda item: item["path"]),
    }


def contact_sheet_html(root, manifest_path):
    manifest = load_json(manifest_path)
    cards = []
    for asset in manifest["assets"]:
        path = html.escape("../" + asset["localPath"])
        name = html.escape(asset["name"])
        meta = html.escape(f"{asset['category']} / {asset['subcategory']}")
        cards.append(
            f'<article class="card"><img src="{path}" alt="{name}"><h2>{name}</h2><p>{meta}</p><code>{html.escape(asset["localPath"])}</code></article>'
        )
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>readme-ux-kit SVG Contact Sheet</title>
  <style>
    :root { color-scheme: light; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body { margin: 0; background: #f8fafc; color: #0f172a; }
    header { position: sticky; top: 0; z-index: 1; padding: 18px 24px; border-bottom: 1px solid #dbe3ef; background: rgba(248, 250, 252, 0.94); backdrop-filter: blur(10px); }
    h1 { margin: 0; font-size: 20px; }
    header p { margin: 6px 0 0; color: #475569; font-size: 13px; }
    main { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; padding: 24px; }
    .card { min-height: 230px; padding: 14px; border: 1px solid #dbe3ef; border-radius: 8px; background: white; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04); }
    img { display: block; width: 100%; height: 132px; object-fit: contain; border: 1px solid #e2e8f0; border-radius: 6px; background: #ffffff; }
    h2 { margin: 12px 0 4px; font-size: 14px; line-height: 1.3; }
    p { margin: 0 0 10px; color: #64748b; font-size: 12px; }
    code { display: block; overflow-wrap: anywhere; color: #334155; font-size: 11px; }
  </style>
</head>
<body>
  <header>
    <h1>readme-ux-kit SVG Contact Sheet</h1>
    <p>Generated from assets/manifest.json for fast visual smoke review.</p>
  </header>
  <main>
""" + "\n".join(cards) + """
  </main>
</body>
</html>
"""


def write_smoke_outputs(output, contact_sheet, root=None, manifest_path=None):
    root = Path(root or repo_root()).resolve()
    manifest_path = Path(manifest_path or root / "assets" / "manifest.json")
    contact_sheet = Path(contact_sheet)
    payload = build_smoke_report(root, manifest_path, rel_path(contact_sheet, root))
    report_path = write_json(output, payload)
    contact_sheet.parent.mkdir(parents=True, exist_ok=True)
    contact_sheet.write_text(contact_sheet_html(root, manifest_path), encoding="utf-8")
    return report_path, contact_sheet, payload["assetCount"]


def check_smoke_outputs(output, contact_sheet, root=None, manifest_path=None):
    root = Path(root or repo_root()).resolve()
    manifest_path = Path(manifest_path or root / "assets" / "manifest.json")
    output = Path(output)
    contact_sheet = Path(contact_sheet)
    payload = build_smoke_report(root, manifest_path, rel_path(contact_sheet, root))
    expected_json = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    expected_html = contact_sheet_html(root, manifest_path)
    failures = []
    if not output.exists():
        failures.append((output, "missing"))
    elif output.read_text(encoding="utf-8") != expected_json:
        failures.append((output, "changed"))
    if not contact_sheet.exists():
        failures.append((contact_sheet, "missing"))
    elif contact_sheet.read_text(encoding="utf-8") != expected_html:
        failures.append((contact_sheet, "changed"))
    invalid_assets = [asset for asset in payload["assets"] if "invalid-svg" in asset["flags"] or "blank-risk" in asset["flags"]]
    return failures, invalid_assets


def render_pngs(root=None, manifest_path=None, png_dir=None, limit=None):
    backend = renderer_backend()
    if backend != "cairosvg":
        return {"backend": backend, "rendered": 0, "skipped": "cairosvg-not-available"}
    import cairosvg

    root = Path(root or repo_root()).resolve()
    manifest = load_json(manifest_path or root / "assets" / "manifest.json")
    png_dir = Path(png_dir or root / "site" / "png")
    png_dir.mkdir(parents=True, exist_ok=True)
    rendered = 0
    for asset in manifest["assets"][: limit or None]:
        source = root / asset["localPath"]
        target = png_dir / (asset["localPath"].replace("/", "__").replace("\\", "__") + ".png")
        cairosvg.svg2png(url=str(source), write_to=str(target))
        rendered += 1
    return {"backend": backend, "rendered": rendered, "skipped": None}


def run_self_tests():
    assert viewbox_status(ET.fromstring('<svg viewBox="0 0 10 20"/>'))["width"] == 10.0
    assert viewbox_status(ET.fromstring("<svg/>"))["risk"] == "missing-viewbox"
    print("svg_smoke_render.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate SVG render smoke metadata and a static contact sheet.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--manifest", default="assets/manifest.json", help="Manifest path relative to repo root.")
    parser.add_argument("--output", default="site/data/svg-render-smoke.json", help="Smoke report path relative to repo root.")
    parser.add_argument("--contact-sheet", default="site/svg-contact-sheet.html", help="Contact sheet path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify smoke outputs are current without writing.")
    parser.add_argument("--png-dir", help="Optional PNG output directory. Requires CairoSVG.")
    parser.add_argument("--png-limit", type=int, help="Optional maximum number of PNG renders.")
    parser.add_argument("--self-test", action="store_true", help="Run focused renderer self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    manifest = root / args.manifest
    output = root / args.output
    contact_sheet = root / args.contact_sheet
    if args.check:
        failures, invalid_assets = check_smoke_outputs(output, contact_sheet, root, manifest)
        for path, status in failures:
            print(f"::error file={rel_path(path, root)}::SVG smoke output is {status}. Run npm run generate:render-smoke.")
        for asset in invalid_assets:
            print(f"::error file={asset['path']}::SVG smoke issue: {', '.join(asset['flags'])}")
        if failures or invalid_assets:
            return 1
        print("SVG render smoke outputs are current.")
        return 0

    report, sheet, count = write_smoke_outputs(output, contact_sheet, root, manifest)
    print(f"Wrote SVG smoke report for {count} asset(s) to {report}")
    print(f"Wrote SVG contact sheet to {sheet}")
    if args.png_dir:
        result = render_pngs(root, manifest, root / args.png_dir, args.png_limit)
        print(f"PNG render result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
