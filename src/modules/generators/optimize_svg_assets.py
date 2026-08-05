from pathlib import Path
import argparse
import re
import sys
import xml.etree.ElementTree as ET


SVG_NAMESPACE = "{http://www.w3.org/2000/svg}"
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
XML_DECL_RE = re.compile(r"^\s*<\?xml[^>]*\?>\s*", re.IGNORECASE)
EXTERNAL_REF_RE = re.compile(r"""(?:href|src)=["']https?://""", re.IGNORECASE)


def safe_optimize_text(content):
    content = content.replace("\ufeff", "")
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    content = XML_DECL_RE.sub("", content)
    content = COMMENT_RE.sub("", content)
    lines = [line.rstrip() for line in content.split("\n")]

    compact_lines = []
    blank_seen = False
    for line in lines:
        if line.strip():
            compact_lines.append(line)
            blank_seen = False
            continue
        if not blank_seen:
            compact_lines.append("")
        blank_seen = True

    return "\n".join(compact_lines).strip() + "\n"


def parse_svg(content):
    try:
        return ET.fromstring(content), None
    except ET.ParseError as error:
        return None, str(error)


def validate_safe_rewrite(original, optimized):
    original_root, original_error = parse_svg(original)
    if original_error:
        return f"original XML is invalid: {original_error}"

    optimized_root, optimized_error = parse_svg(optimized)
    if optimized_error:
        return f"optimized XML would be invalid: {optimized_error}"

    if original_root.tag != f"{SVG_NAMESPACE}svg" or optimized_root.tag != f"{SVG_NAMESPACE}svg":
        return "root element is not <svg>"

    if original_root.attrib.get("viewBox") != optimized_root.attrib.get("viewBox"):
        return "optimized SVG would change viewBox"

    lowered = optimized.lower()
    if "<script" in lowered:
        return "optimized SVG would contain <script>"
    if EXTERNAL_REF_RE.search(optimized):
        return "optimized SVG would contain external href/src reference"

    return None


def optimize_file(path, write=False):
    original = path.read_text(encoding="utf-8")
    optimized = safe_optimize_text(original)
    if optimized == original:
        return None

    issue = validate_safe_rewrite(original, optimized)
    if write and not issue:
        path.write_text(optimized, encoding="utf-8")

    return {
        "path": path,
        "before": len(original.encode("utf-8")),
        "after": len(optimized.encode("utf-8")),
        "issue": issue,
    }


def collect_results(assets_dir, write=False):
    svg_files = sorted(assets_dir.rglob("*.svg"), key=lambda path: path.as_posix().lower())
    return [result for path in svg_files if (result := optimize_file(path, write=write))]


def print_results(results, write=False):
    if not results:
        print("SVG assets already match the safe optimization profile.")
        return

    valid_results = [result for result in results if not result["issue"]]
    invalid_results = [result for result in results if result["issue"]]
    saved_bytes = sum(result["before"] - result["after"] for result in valid_results)
    action = "Optimized" if write else "Would optimize"

    if saved_bytes >= 0:
        print(f"{action} {len(valid_results)} SVG asset(s), saving {saved_bytes} byte(s).")
    else:
        print(f"{action} {len(valid_results)} SVG asset(s), adding {-saved_bytes} byte(s).")
    for result in valid_results[:25]:
        delta = result["before"] - result["after"]
        if delta >= 0:
            print(f"- {result['path'].as_posix()} ({delta} bytes saved)")
        else:
            print(f"- {result['path'].as_posix()} ({-delta} bytes added)")
    if len(valid_results) > 25:
        print(f"... and {len(valid_results) - 25} more")

    if invalid_results:
        print()
        print("Skipped unsafe rewrite candidate(s):")
        for result in invalid_results:
            print(f"- {result['path'].as_posix()}: {result['issue']}")


def main():
    parser = argparse.ArgumentParser(description="Safely optimize SVG assets without changing animation semantics.")
    parser.add_argument("--assets-dir", default="assets", help="Asset directory to scan.")
    parser.add_argument("--write", action="store_true", help="Rewrite SVG files using the safe optimization profile.")
    parser.add_argument("--check", action="store_true", help="Report SVGs that could be changed without writing files.")
    parser.add_argument("--strict", action="store_true", help="Fail if any SVG could be changed by the safe optimization profile.")
    args = parser.parse_args()

    assets_dir = Path(args.assets_dir)
    if not assets_dir.exists():
        print(f"Assets directory does not exist: {assets_dir}", file=sys.stderr)
        return 1

    results = collect_results(assets_dir, write=args.write)
    print_results(results, write=args.write)

    if any(result["issue"] for result in results):
        return 1
    if args.strict and results:
        print()
        print("Run `npm run optimize:svg` to apply the safe optimization profile.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
