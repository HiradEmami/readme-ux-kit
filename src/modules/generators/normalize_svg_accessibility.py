from pathlib import Path
import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET


ROOT_TAG_RE = re.compile(r"<svg\b[^>]*>", re.IGNORECASE | re.DOTALL)
ANIMATION_RE = re.compile(r"<(?:animate|animateMotion|animateTransform|set)\b|\banimation\s*:", re.IGNORECASE)
ACRONYMS = {
    "ai": "AI",
    "api": "API",
    "ci": "CI",
    "cli": "CLI",
    "cpu": "CPU",
    "css": "CSS",
    "gpu": "GPU",
    "html": "HTML",
    "http": "HTTP",
    "js": "JS",
    "json": "JSON",
    "ml": "ML",
    "npm": "npm",
    "pdf": "PDF",
    "sdk": "SDK",
    "svg": "SVG",
    "ui": "UI",
    "url": "URL",
    "ux": "UX",
    "yaml": "YAML",
}


def local_name(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def humanize(stem):
    words = []
    for part in re.split(r"[_-]+", stem):
        lowered = part.lower()
        words.append(ACRONYMS.get(lowered, lowered.capitalize()))
    return " ".join(words)


def set_root_attribute(opening_tag, name, value):
    pattern = re.compile(rf"(?P<prefix>\s){re.escape(name)}\s*=\s*(?P<quote>[\"']).*?(?P=quote)", re.IGNORECASE | re.DOTALL)
    replacement = rf'\g<prefix>{name}="{value}"'
    if pattern.search(opening_tag):
        return pattern.sub(replacement, opening_tag, count=1)
    return opening_tag[:-1].rstrip() + f' {name}="{value}">'


def metadata_indent(content, opening_match):
    remainder = content[opening_match.end() :]
    match = re.match(r"\r?\n(?P<indent>[ \t]+)", remainder)
    return match.group("indent") if match else "  "


def enrich_svg(content, stem):
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        raise ValueError(f"invalid XML: {error}") from error

    opening_match = ROOT_TAG_RE.search(content)
    if opening_match is None:
        raise ValueError("missing root <svg> element")

    title_exists = any(local_name(element.tag) == "title" for element in root.iter())
    desc_exists = any(local_name(element.tag) == "desc" for element in root.iter())
    title = humanize(stem)
    motion = "animated" if ANIMATION_RE.search(content) else "static"
    article = "An" if motion == "animated" else "A"
    description = f"{article} {motion} README SVG asset illustrating {title}."
    indent = metadata_indent(content, opening_match)
    newline = "\r\n" if "\r\n" in content else "\n"

    opening_tag = set_root_attribute(opening_match.group(0), "role", "img")
    result = content[: opening_match.start()] + opening_tag + content[opening_match.end() :]
    insertion_offset = opening_match.start() + len(opening_tag)

    additions = []
    if not title_exists:
        additions.append(f"{indent}<title>{html.escape(title)}</title>")
    if not desc_exists:
        additions.append(f"{indent}<desc>{html.escape(description)}</desc>")
    if additions:
        result = result[:insertion_offset] + newline + newline.join(additions) + result[insertion_offset:]
    return result


def changed_assets(assets_dir, write=False):
    changed = []
    failures = []
    for path in sorted(assets_dir.rglob("*.svg"), key=lambda item: item.as_posix().lower()):
        content = path.read_text(encoding="utf-8")
        try:
            updated = enrich_svg(content, path.stem)
        except ValueError as error:
            failures.append((path, str(error)))
            continue
        if updated == content:
            continue
        changed.append(path)
        if write:
            path.write_text(updated, encoding="utf-8", newline="")
    return changed, failures


def run_self_tests():
    source = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">\n  <path d="M0 0h10v10H0z"/>\n</svg>\n'
    updated = enrich_svg(source, "icon_api_status")
    assert 'role="img"' in updated
    assert "<title>Icon API Status</title>" in updated
    assert "<desc>A static README SVG asset illustrating Icon API Status.</desc>" in updated
    assert enrich_svg(updated, "icon_api_status") == updated

    labelled = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" role="presentation">\n  <title>Custom</title>\n  <animate attributeName="opacity" dur="1s"/>\n</svg>'
    updated = enrich_svg(labelled, "loading_orbit")
    assert updated.count("<title>") == 1
    assert 'role="img"' in updated
    assert "<desc>An animated README" in updated
    print("normalize_svg_accessibility.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Add consistent accessibility metadata to SVG assets.")
    parser.add_argument("--assets-dir", default="assets", help="Asset directory to scan.")
    parser.add_argument("--write", action="store_true", help="Update SVG files in place.")
    parser.add_argument("--check", action="store_true", help="Fail when SVG accessibility metadata is incomplete.")
    parser.add_argument("--self-test", action="store_true", help="Run normalizer self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0
    if args.write and args.check:
        parser.error("--write and --check cannot be used together")

    assets_dir = Path(args.assets_dir)
    if not assets_dir.exists():
        print(f"Assets directory does not exist: {assets_dir}", file=sys.stderr)
        return 1

    changed, failures = changed_assets(assets_dir, write=args.write)
    for path, error in failures:
        print(f"::error file={path.as_posix()}::{error}")
    if failures:
        return 1

    if args.write:
        print(f"Updated accessibility metadata in {len(changed)} SVG asset(s).")
        return 0
    if args.check and changed:
        preview = ", ".join(path.as_posix() for path in changed[:10])
        suffix = "" if len(changed) <= 10 else f", and {len(changed) - 10} more"
        print(f"::error::Accessibility metadata is incomplete in {len(changed)} SVG asset(s): {preview}{suffix}")
        print("Run npm run normalize:svg:accessibility.")
        return 1

    print("SVG accessibility metadata is current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
