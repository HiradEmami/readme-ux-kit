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

    role = root.attrib.get("role")
    title_elements = [element for element in root.iter() if element.tag == f"{SVG_NAMESPACE}title"]
    desc_elements = [element for element in root.iter() if element.tag == f"{SVG_NAMESPACE}desc"]
    aria_label = root.attrib.get("aria-label", "").strip()
    aria_labelledby = root.attrib.get("aria-labelledby", "").strip()
    element_ids = {element.attrib["id"] for element in root.iter() if element.attrib.get("id")}

    if role != "img":
        issues.append('missing role="img"')
    if not aria_label and not aria_labelledby and not title_elements:
        issues.append("missing accessible name")
    if aria_labelledby and not all(reference in element_ids for reference in aria_labelledby.split()):
        issues.append("aria-labelledby references a missing element")
    if not desc_elements:
        issues.append("missing <desc>")

    if "<script" in content.lower():
        issues.append("contains <script>")

    if EXTERNAL_REF.search(content):
        issues.append("contains external href/src reference")

    return issues


def run_self_tests():
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "asset.svg"
        path.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" role="img" aria-labelledby="title desc">'
            '<title id="title">Sample</title><desc id="desc">Sample description.</desc><path d="M0 0h10v10H0z"/>'
            '</svg>',
            encoding="utf-8",
        )
        assert validate_svg(path) == []
        path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"/>', encoding="utf-8")
        issues = validate_svg(path)
        assert 'missing role="img"' in issues
        assert "missing accessible name" in issues
        assert "missing <desc>" in issues
    print("validate_svg_assets.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Validate SVG assets for repository safety and portability.")
    parser.add_argument("--assets-dir", default="assets", help="Asset directory to scan.")
    parser.add_argument("--self-test", action="store_true", help="Run validator self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

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
