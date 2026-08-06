from pathlib import Path
import argparse
import re
import sys
import xml.etree.ElementTree as ET


SVG_NAMESPACE = "{http://www.w3.org/2000/svg}"
EXTERNAL_REF = re.compile(r"""(?:href|src)=["']https?://""", re.IGNORECASE)


def validate_svg(path):
    issues = []
    content = path.read_text(encoding="utf-8")

    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        return [f"invalid XML: {error}"]

    if root.tag != f"{SVG_NAMESPACE}svg":
        issues.append("root element is not <svg>")

    if not root.attrib.get("viewBox"):
        issues.append("missing viewBox")

    if "<script" in content.lower():
        issues.append("contains <script>")

    if EXTERNAL_REF.search(content):
        issues.append("contains external href/src reference")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate SVG assets for repository safety and portability.")
    parser.add_argument("--assets-dir", default="assets", help="Asset directory to scan.")
    args = parser.parse_args()

    assets_root = Path(args.assets_dir)
    if not assets_root.exists():
        print(f"Assets directory does not exist: {assets_root}", file=sys.stderr)
        return 1

    failures = []
    svg_files = sorted(assets_root.rglob("*.svg"), key=lambda path: path.as_posix().lower())

    for svg_file in svg_files:
        issues = validate_svg(svg_file)
        if issues:
            failures.append((svg_file, issues))

    if failures:
        print("SVG validation failed:")
        print()
        for svg_file, issues in failures:
            print(f"- {svg_file.as_posix()}")
            for issue in issues:
                print(f"  - {issue}")
        return 1

    print(f"Validated {len(svg_files)} SVG assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
