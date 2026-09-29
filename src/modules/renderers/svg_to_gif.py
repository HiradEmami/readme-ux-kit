from pathlib import Path
import argparse
import asyncio
import hashlib
import html
import importlib.util
import io
import json
import re
import sys
import xml.etree.ElementTree as ET

from src.modules.common.repo import load_json, rel_path, repo_root, write_json
from src.modules.generators.generate_asset_previews import DEFAULT_REPO_RAW_BASE, animation_label, clean_asset_name


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/renderers/svg_to_gif.py"
DEFAULT_OUTPUT_DIR = "output/gifs"
DEFAULT_INDEX_OUTPUT = "output/gifs/index.json"
DEFAULT_DURATION_MS = 1600
DEFAULT_FPS = 16
DEFAULT_MAX_WIDTH = 960
DEFAULT_MAX_HEIGHT = 360
DEFAULT_MIN_WIDTH = 240
DEFAULT_MIN_HEIGHT = 120
DEFAULT_BACKGROUND = "#ffffff"


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_number(value):
    if value is None:
        return None
    match = re.match(r"^\s*([0-9]+(?:\.[0-9]+)?)", value)
    return float(match.group(1)) if match else None


def dimensions_from_svg_root(svg_root):
    viewbox = svg_root.attrib.get("viewBox")
    if viewbox:
        parts = viewbox.replace(",", " ").split()
        if len(parts) == 4:
            try:
                width = float(parts[2])
                height = float(parts[3])
                if width > 0 and height > 0:
                    return {"width": width, "height": height, "viewBox": viewbox}
            except ValueError:
                pass

    width = parse_number(svg_root.attrib.get("width"))
    height = parse_number(svg_root.attrib.get("height"))
    if width and height and width > 0 and height > 0:
        return {"width": width, "height": height, "viewBox": viewbox or f"0 0 {width:g} {height:g}"}

    return {"width": 640.0, "height": 160.0, "viewBox": viewbox or "0 0 640 160"}


def parse_dimensions_from_markup(svg_markup):
    return dimensions_from_svg_root(ET.fromstring(svg_markup))


def parse_dimensions(svg_path):
    return parse_dimensions_from_markup(Path(svg_path).read_text(encoding="utf-8"))


def scaled_size(
    dimensions,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
    min_width=DEFAULT_MIN_WIDTH,
    min_height=DEFAULT_MIN_HEIGHT,
):
    width = dimensions["width"]
    height = dimensions["height"]
    scale = 1.0
    if width < min_width or height < min_height:
        scale = max(min_width / width, min_height / height)
    scale = min(scale, max_width / width, max_height / height)
    return {
        "width": max(24, int(round(width * scale))),
        "height": max(24, int(round(height * scale))),
    }


def gif_relative_path(asset_path):
    relative = Path(asset_path).with_suffix("").as_posix()
    if relative.startswith("assets/"):
        relative = relative[len("assets/") :]
    return f"{relative}.gif"


def frame_plan(duration_ms=DEFAULT_DURATION_MS, fps=DEFAULT_FPS):
    frame_count = max(1, round(duration_ms / (1000 / fps)))
    return frame_count, round(duration_ms / frame_count)


def raw_url(raw_base, local_path):
    return f"{raw_base.rstrip('/')}/{local_path.lstrip('/')}"


def markdown_image(label, url):
    return f"![{label}]({url})"


def html_image(label, url):
    return f'<img src="{html.escape(url, quote=True)}" alt="{html.escape(label, quote=True)}" />'


def load_manifest(root, manifest_path):
    manifest_path = Path(manifest_path)
    if not manifest_path.is_absolute():
        manifest_path = Path(root) / manifest_path
    if manifest_path.exists():
        return load_json(manifest_path)

    from src.modules.generators.asset_manifest import build_manifest

    return build_manifest(Path(root), Path("assets"))


def select_assets(manifest, requested_assets=None):
    if not requested_assets:
        raise ValueError("Provide at least one SVG path with --asset for GIF export.")
    records_by_path = {asset["localPath"]: asset for asset in manifest["assets"]}
    selected_paths = list(requested_assets)
    missing = [path for path in selected_paths if path not in records_by_path]
    if missing:
        raise FileNotFoundError(f"GIF export source asset(s) missing from manifest: {', '.join(missing)}")
    return [records_by_path[path] for path in selected_paths]


def build_gif_index(
    root=None,
    manifest_path="assets/manifest.json",
    output_dir=DEFAULT_OUTPUT_DIR,
    raw_base=DEFAULT_REPO_RAW_BASE,
    requested_assets=None,
    duration_ms=DEFAULT_DURATION_MS,
    fps=DEFAULT_FPS,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
    min_width=DEFAULT_MIN_WIDTH,
    min_height=DEFAULT_MIN_HEIGHT,
    background=DEFAULT_BACKGROUND,
):
    root = Path(root or repo_root()).resolve()
    manifest = load_manifest(root, manifest_path)
    selected = select_assets(manifest, requested_assets)
    frame_count, frame_delay_ms = frame_plan(duration_ms, fps)

    assets = []
    for asset in selected:
        local_path = asset["localPath"]
        source = root / local_path
        dimensions = parse_dimensions(source)
        render_size = scaled_size(
            dimensions,
            max_width=max_width,
            max_height=max_height,
            min_width=min_width,
            min_height=min_height,
        )
        gif_path = f"{Path(output_dir).as_posix().rstrip('/')}/{gif_relative_path(local_path)}"
        svg_raw_url = asset.get("rawUrl") or raw_url(raw_base, local_path)
        gif_raw_url = raw_url(raw_base, gif_path)
        label = clean_asset_name(source)
        assets.append(
            {
                "name": label,
                "category": asset.get("category"),
                "subcategory": asset.get("subcategory"),
                "localPath": local_path,
                "sourceSha256": sha256_file(source),
                "sourceType": animation_label(source),
                "svgRawUrl": svg_raw_url,
                "gifPath": gif_path,
                "gifRawUrl": gif_raw_url,
                "dimensions": {
                    "sourceWidth": dimensions["width"],
                    "sourceHeight": dimensions["height"],
                    "viewBox": dimensions["viewBox"],
                    "renderWidth": render_size["width"],
                    "renderHeight": render_size["height"],
                },
                "qualityProfile": "gif-friendly-flat-motion",
                "copy": {
                    "markdownSvg": markdown_image(label, svg_raw_url),
                    "markdownGif": markdown_image(f"{label} GIF fallback", gif_raw_url),
                    "htmlSvg": html_image(label, svg_raw_url),
                    "htmlGif": html_image(f"{label} GIF fallback", gif_raw_url),
                },
            }
        )

    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "assetCount": len(assets),
        "outputDir": Path(output_dir).as_posix(),
        "galleryPath": f"{Path(output_dir).as_posix().rstrip('/')}/README.md",
        "renderSettings": {
            "durationMs": duration_ms,
            "fps": fps,
            "frameCount": frame_count,
            "frameDelayMs": frame_delay_ms,
            "maxWidth": max_width,
            "maxHeight": max_height,
            "minWidth": min_width,
            "minHeight": min_height,
            "background": background,
        },
        "assets": assets,
    }


def require_module(module_name, package_name):
    if importlib.util.find_spec(module_name) is None:
        raise RuntimeError(
            f"Missing dependency `{package_name}`. Install the src project dependencies, then rerun this command."
        )


def require_render_dependencies():
    require_module("PIL", "Pillow")
    require_module("playwright", "playwright")


def require_check_dependencies():
    require_module("PIL", "Pillow")


def preview_html(svg_markup, width, height, background):
    if background == "transparent":
        background_css = "transparent"
    else:
        background_css = background
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    html, body {{
      width: {width}px;
      height: {height}px;
      margin: 0;
      overflow: hidden;
      background: {background_css};
    }}
    #asset-stage {{
      display: block;
      width: {width}px;
      height: {height}px;
      background: {background_css};
    }}
    #asset-stage > svg {{
      display: block;
      width: 100%;
      height: 100%;
      max-width: 100%;
      max-height: 100%;
    }}
  </style>
</head>
<body>
  <div id="asset-stage">
{svg_markup}
  </div>
</body>
</html>
"""


async def capture_svg_markup_png_frames(svg_markup, width, height, frame_count, frame_delay_ms, background):
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
            reduced_motion="no-preference",
        )
        await page.set_content(preview_html(svg_markup, width, height, background), wait_until="load")
        stage = page.locator("#asset-stage")
        await stage.wait_for(state="visible")
        await page.wait_for_timeout(100)
        frames = []
        for _ in range(frame_count):
            frames.append(await stage.screenshot(type="png", omit_background=background == "transparent"))
            await page.wait_for_timeout(frame_delay_ms)
        await browser.close()
    return frames


async def capture_png_frames(asset_record, root, frame_delay_ms, background):
    width = asset_record["dimensions"]["renderWidth"]
    height = asset_record["dimensions"]["renderHeight"]
    source = (Path(root) / asset_record["localPath"]).resolve()
    svg_markup = source.read_text(encoding="utf-8")
    return await capture_svg_markup_png_frames(
        svg_markup,
        width,
        height,
        asset_record["_frameCount"],
        frame_delay_ms,
        background,
    )


def flatten_frame(image, background):
    from PIL import Image

    if background == "transparent":
        matte = Image.new("RGBA", image.size, "#ffffff")
    else:
        matte = Image.new("RGBA", image.size, background)
    matte.alpha_composite(image)
    return matte.convert("RGB")


def global_palette(frames):
    from PIL import Image

    if len(frames) == 1:
        return frames[0].quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    width = max(frame.width for frame in frames)
    height = sum(frame.height for frame in frames)
    sheet = Image.new("RGB", (width, height), "#ffffff")
    y = 0
    for frame in frames:
        sheet.paste(frame, (0, y))
        y += frame.height
    return sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT)


def frames_to_gif(png_frames, output_path, frame_delay_ms, background):
    from PIL import Image

    rgb_frames = []
    for frame in png_frames:
        image = Image.open(io.BytesIO(frame)).convert("RGBA")
        rgb_frames.append(flatten_frame(image, background))

    palette = global_palette(rgb_frames)
    frames = [
        frame.quantize(palette=palette, dither=Image.Dither.NONE)
        for frame in rgb_frames
    ]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_delay_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )


def render_svg_markup_to_gif(
    svg_markup,
    output_path,
    duration_ms=DEFAULT_DURATION_MS,
    fps=DEFAULT_FPS,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
    min_width=DEFAULT_MIN_WIDTH,
    min_height=DEFAULT_MIN_HEIGHT,
    background=DEFAULT_BACKGROUND,
):
    require_render_dependencies()
    dimensions = parse_dimensions_from_markup(svg_markup)
    render_size = scaled_size(
        dimensions,
        max_width=max_width,
        max_height=max_height,
        min_width=min_width,
        min_height=min_height,
    )
    frame_count, frame_delay_ms = frame_plan(duration_ms, fps)
    png_frames = asyncio.run(
        capture_svg_markup_png_frames(
            svg_markup,
            render_size["width"],
            render_size["height"],
            frame_count,
            frame_delay_ms,
            background,
        )
    )
    frames_to_gif(png_frames, output_path, frame_delay_ms, background)
    return {
        "renderSettings": {
            "durationMs": duration_ms,
            "fps": fps,
            "frameCount": frame_count,
            "frameDelayMs": frame_delay_ms,
            "maxWidth": max_width,
            "maxHeight": max_height,
            "minWidth": min_width,
            "minHeight": min_height,
            "background": background,
        },
        "dimensions": {
            "sourceWidth": dimensions["width"],
            "sourceHeight": dimensions["height"],
            "viewBox": dimensions["viewBox"],
            "renderWidth": render_size["width"],
            "renderHeight": render_size["height"],
        },
    }


async def render_gifs(payload, root):
    settings = payload["renderSettings"]
    for asset in payload["assets"]:
        asset["_frameCount"] = settings["frameCount"]
        output = Path(root) / asset["gifPath"]
        png_frames = await capture_png_frames(asset, root, settings["frameDelayMs"], settings["background"])
        frames_to_gif(png_frames, output, settings["frameDelayMs"], settings["background"])
        del asset["_frameCount"]


def remove_extra_gifs(root, output_dir, expected_paths):
    output_root = Path(root) / output_dir
    if not output_root.exists():
        return []
    expected = {(Path(root) / path).resolve() for path in expected_paths}
    removed = []
    for path in output_root.rglob("*.gif"):
        if path.resolve() not in expected:
            path.unlink()
            removed.append(path)
    return removed


def gallery_markdown(payload):
    output_dir = Path(payload["outputDir"])
    lines = [
        "# Local GIF exports",
        "",
        "Generated local GIF exports from selected SVG assets. This output is intended for local use and should not be committed unless you intentionally want to publish it.",
        "",
        "SVG remains the primary copy format. Use exported GIFs only when an animated fallback or downloadable preview is useful.",
        "",
        "## Index",
        "",
        "| GIF | Source SVG | Size |",
        "| --- | --- | ---: |",
    ]
    for asset in payload["assets"]:
        gif_relative = Path(asset["gifPath"]).relative_to(output_dir).as_posix()
        source_link = f"../../{asset['localPath']}"
        size = f'{asset["dimensions"]["renderWidth"]}x{asset["dimensions"]["renderHeight"]}'
        lines.append(f"| ![{asset['name']}](./{gif_relative}) | [`{asset['localPath']}`]({source_link}) | {size} |")

    lines.extend(["", "## Copy Snippets", ""])
    for asset in payload["assets"]:
        gif_relative = Path(asset["gifPath"]).relative_to(output_dir).as_posix()
        source_link = f"../../{asset['localPath']}"
        lines.extend(
            [
                f"### {asset['name']}",
                "",
                f"![{asset['name']}](./{gif_relative})",
                "",
                f"- Source SVG: [`{asset['localPath']}`]({source_link})",
                f"- GIF path: `{asset['gifPath']}`",
                f"- Quality profile: `{asset['qualityProfile']}`",
                "",
                "<details>",
                "<summary>Markdown SVG</summary>",
                "",
                "```markdown",
                asset["copy"]["markdownSvg"],
                "```",
                "",
                "</details>",
                "",
                "<details>",
                "<summary>Markdown GIF</summary>",
                "",
                "```markdown",
                asset["copy"]["markdownGif"],
                "```",
                "",
                "</details>",
                "",
                "<details>",
                "<summary>HTML SVG</summary>",
                "",
                "```html",
                asset["copy"]["htmlSvg"],
                "```",
                "",
                "</details>",
                "",
                "<details>",
                "<summary>HTML GIF</summary>",
                "",
                "```html",
                asset["copy"]["htmlGif"],
                "```",
                "",
                "</details>",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_gif_exports(
    index_output,
    root=None,
    manifest_path="assets/manifest.json",
    output_dir=DEFAULT_OUTPUT_DIR,
    raw_base=DEFAULT_REPO_RAW_BASE,
    requested_assets=None,
    duration_ms=DEFAULT_DURATION_MS,
    fps=DEFAULT_FPS,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
    min_width=DEFAULT_MIN_WIDTH,
    min_height=DEFAULT_MIN_HEIGHT,
    background=DEFAULT_BACKGROUND,
    clean=False,
):
    root = Path(root or repo_root()).resolve()
    index_output = Path(index_output)
    if not index_output.is_absolute():
        index_output = root / index_output
    require_render_dependencies()
    payload = build_gif_index(
        root,
        manifest_path=manifest_path,
        output_dir=output_dir,
        raw_base=raw_base,
        requested_assets=requested_assets,
        duration_ms=duration_ms,
        fps=fps,
        max_width=max_width,
        max_height=max_height,
        min_width=min_width,
        min_height=min_height,
        background=background,
    )
    asyncio.run(render_gifs(payload, root))
    if clean:
        remove_extra_gifs(root, output_dir, [asset["gifPath"] for asset in payload["assets"]])
    gallery_path = root / payload["galleryPath"]
    gallery_path.parent.mkdir(parents=True, exist_ok=True)
    gallery_path.write_text(gallery_markdown(payload), encoding="utf-8")
    write_json(index_output, payload)
    return Path(index_output), payload["assetCount"]


def validate_gif(path, expected_frames):
    from PIL import Image

    with Image.open(path) as image:
        if image.format != "GIF":
            return "not-gif"
        if getattr(image, "n_frames", 1) < min(expected_frames, 2):
            return "single-frame"
    return None


def check_gif_exports(
    index_output,
    root=None,
    manifest_path="assets/manifest.json",
    output_dir=DEFAULT_OUTPUT_DIR,
    raw_base=DEFAULT_REPO_RAW_BASE,
    requested_assets=None,
    duration_ms=DEFAULT_DURATION_MS,
    fps=DEFAULT_FPS,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
    min_width=DEFAULT_MIN_WIDTH,
    min_height=DEFAULT_MIN_HEIGHT,
    background=DEFAULT_BACKGROUND,
):
    root = Path(root or repo_root()).resolve()
    index_output = Path(index_output)
    if not index_output.is_absolute():
        index_output = root / index_output
    require_check_dependencies()
    payload = build_gif_index(
        root,
        manifest_path=manifest_path,
        output_dir=output_dir,
        raw_base=raw_base,
        requested_assets=requested_assets,
        duration_ms=duration_ms,
        fps=fps,
        max_width=max_width,
        max_height=max_height,
        min_width=min_width,
        min_height=min_height,
        background=background,
    )
    expected_json = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    failures = []
    if not index_output.exists():
        failures.append((index_output, "missing"))
    elif index_output.read_text(encoding="utf-8") != expected_json:
        failures.append((index_output, "changed"))

    gallery_path = root / payload["galleryPath"]
    expected_gallery = gallery_markdown(payload)
    if not gallery_path.exists():
        failures.append((gallery_path, "missing"))
    elif gallery_path.read_text(encoding="utf-8") != expected_gallery:
        failures.append((gallery_path, "changed"))

    expected_paths = {asset["gifPath"] for asset in payload["assets"]}
    for asset in payload["assets"]:
        path = root / asset["gifPath"]
        if not path.exists():
            failures.append((path, "missing"))
            continue
        issue = validate_gif(path, payload["renderSettings"]["frameCount"])
        if issue:
            failures.append((path, issue))

    output_root = root / output_dir
    if output_root.exists():
        for gif in output_root.rglob("*.gif"):
            relative = rel_path(gif, root)
            if relative not in expected_paths:
                failures.append((gif, "extra"))

    return failures


def parse_asset_args(values):
    if not values:
        return None
    assets = []
    for value in values:
        assets.extend(part.strip().replace("\\", "/") for part in value.split(",") if part.strip())
    return assets


def print_check_failures(failures, root):
    print("GIF exports are stale or invalid. Regenerate them with the same export command and arguments:")
    print()
    print("  npm run export:gif -- --asset assets/path/to/asset.svg")
    print()
    for path, status in failures[:30]:
        rel = rel_path(path, root) if Path(path).is_absolute() else Path(path).as_posix()
        print(f"- {rel}: {status}")
        print(f"::error file={rel}::GIF export is {status}.")
    if len(failures) > 30:
        print(f"... and {len(failures) - 30} more")


def run_self_tests():
    assert gif_relative_path("assets/loadings/loading_neural_synapse.svg") == "loadings/loading_neural_synapse.gif"
    assert frame_plan(1600, 16) == (26, 62)
    assert scaled_size({"width": 1440.0, "height": 360.0}, max_width=960, max_height=360) == {
        "width": 960,
        "height": 240,
    }
    assert scaled_size({"width": 80.0, "height": 80.0}, min_width=240, min_height=120) == {
        "width": 240,
        "height": 240,
    }
    assert parse_dimensions_from_markup('<svg viewBox="0 0 100 40"></svg>') == {
        "width": 100.0,
        "height": 40.0,
        "viewBox": "0 0 100 40",
    }
    assert parse_asset_args(["assets/a.svg,assets/b.svg"]) == ["assets/a.svg", "assets/b.svg"]
    try:
        select_assets({"assets": []})
        raise AssertionError("select_assets should require explicit assets")
    except ValueError:
        pass
    assert markdown_image("Demo", "https://example.com/demo.gif") == "![Demo](https://example.com/demo.gif)"
    print("svg_to_gif.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Export selected SVG assets to local animated GIF files.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--manifest", default="assets/manifest.json", help="Asset manifest path relative to repo root.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="GIF output directory relative to repo root.")
    parser.add_argument("--index-output", default=DEFAULT_INDEX_OUTPUT, help="GIF export index path relative to repo root.")
    parser.add_argument("--raw-base", default=DEFAULT_REPO_RAW_BASE, help="Raw GitHub base URL.")
    parser.add_argument("--asset", action="append", help="Asset path to export. Can be repeated or comma-separated.")
    parser.add_argument("--duration-ms", type=int, default=DEFAULT_DURATION_MS, help="Animation capture duration in milliseconds.")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="GIF frames per second.")
    parser.add_argument("--max-width", type=int, default=DEFAULT_MAX_WIDTH, help="Maximum render width.")
    parser.add_argument("--max-height", type=int, default=DEFAULT_MAX_HEIGHT, help="Maximum render height.")
    parser.add_argument("--min-width", type=int, default=DEFAULT_MIN_WIDTH, help="Minimum render width before max constraints.")
    parser.add_argument("--min-height", type=int, default=DEFAULT_MIN_HEIGHT, help="Minimum render height before max constraints.")
    parser.add_argument("--background", default=DEFAULT_BACKGROUND, help="CSS background color or `transparent`.")
    parser.add_argument("--clean", action="store_true", help="Remove obsolete GIFs from the output directory.")
    parser.add_argument("--check", action="store_true", help="Verify GIF exports and index freshness without rendering.")
    parser.add_argument("--self-test", action="store_true", help="Run focused GIF exporter self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    if (
        args.duration_ms <= 0
        or args.fps <= 0
        or args.max_width <= 0
        or args.max_height <= 0
        or args.min_width <= 0
        or args.min_height <= 0
    ):
        print("duration, fps, max width, max height, min width, and min height must be positive.", file=sys.stderr)
        return 2

    root = Path(args.repo_root).resolve()
    requested_assets = parse_asset_args(args.asset)
    index_output = root / args.index_output

    try:
        if args.check:
            failures = check_gif_exports(
                index_output,
                root=root,
                manifest_path=args.manifest,
                output_dir=args.output_dir,
                raw_base=args.raw_base,
                requested_assets=requested_assets,
                duration_ms=args.duration_ms,
                fps=args.fps,
                max_width=args.max_width,
                max_height=args.max_height,
                min_width=args.min_width,
                min_height=args.min_height,
                background=args.background,
            )
            if failures:
                print_check_failures(failures, root)
                return 1
            print("GIF exports are current.")
            return 0

        output, count = write_gif_exports(
            index_output,
            root=root,
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            raw_base=args.raw_base,
            requested_assets=requested_assets,
            duration_ms=args.duration_ms,
            fps=args.fps,
            max_width=args.max_width,
            max_height=args.max_height,
            min_width=args.min_width,
            min_height=args.min_height,
            background=args.background,
            clean=args.clean,
        )
    except (RuntimeError, FileNotFoundError, ValueError, ET.ParseError) as error:
        print(error, file=sys.stderr)
        return 2

    print(f"Wrote {count} GIF export(s).")
    print(f"Wrote GIF export index to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
