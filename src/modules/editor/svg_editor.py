from pathlib import Path
import argparse
import json
import re
import tempfile
import xml.etree.ElementTree as ET

from src.modules.common.repo import rel_path, repo_root, write_json
from src.modules.generators.svg_editor_metadata import local_name
from src.modules.generators.validate_svg_assets import validate_svg


ET.register_namespace("", "http://www.w3.org/2000/svg")

SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/editor/svg_editor.py"
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b")
DURATION_RE = re.compile(r"(?P<number>\d+(?:\.\d+)?)(?P<unit>ms|s)\b")


def normalize_color(value):
    value = value.strip().lower()
    if not value.startswith("#"):
        value = f"#{value}"
    if len(value) == 4:
        value = "#" + "".join(character * 2 for character in value[1:])
    if not re.fullmatch(r"#[0-9a-f]{6}", value):
        raise ValueError(f"Invalid hex color: {value}")
    return value


def normalize_color_map(mapping):
    return {normalize_color(source): normalize_color(target) for source, target in mapping.items()}


def replace_colors(source, color_map):
    normalized = normalize_color_map(color_map)

    def replace(match):
        value = normalize_color(match.group(0))
        return normalized.get(value, match.group(0))

    return HEX_COLOR_RE.sub(replace, source)


def element_edit_id(element):
    return element.attrib.get("data-edit-id") or element.attrib.get("data-editor-id") or element.attrib.get("data-id")


def text_identity(element, semantic_path, numeric_path):
    return {
        element_edit_id(element),
        element.attrib.get("id"),
        semantic_path,
        numeric_path,
        "".join(element.itertext()).strip(),
    }


def iter_with_paths(root):
    def walk(element, semantic_path, numeric_path):
        yield element, semantic_path, numeric_path
        child_counts = {}
        children = [child for child in list(element) if isinstance(child.tag, str)]
        for index, child in enumerate(children):
            tag = local_name(child.tag)
            child_counts[tag] = child_counts.get(tag, 0) + 1
            yield from walk(child, f"{semantic_path}/{tag}[{child_counts[tag]}]", f"{numeric_path}.{index}")

    yield from walk(root, local_name(root.tag) or "svg", "0")


def replace_text(root, replacements):
    changed = 0
    for element, semantic_path, numeric_path in iter_with_paths(root):
        if local_name(element.tag) not in {"text", "tspan", "textPath"}:
            continue
        identities = text_identity(element, semantic_path, numeric_path)
        current = "".join(element.itertext()).strip()
        for replacement in replacements:
            target = replacement.get("target") or replacement.get("from") or replacement.get("editId") or replacement.get("id") or replacement.get("nodePath")
            if target in identities:
                element.text = replacement["to"]
                for child in list(element):
                    child.tail = None
                changed += 1
                break
            if replacement.get("from") and current == replacement["from"]:
                element.text = replacement["to"]
                changed += 1
                break
    return changed


def remove_elements(root, targets):
    parent_map = {child: parent for parent in root.iter() for child in list(parent)}
    remove_nodes = []
    for element, semantic_path, numeric_path in iter_with_paths(root):
        identities = {element_edit_id(element), element.attrib.get("id"), semantic_path, numeric_path}
        if identities & set(targets):
            remove_nodes.append(element)
    removed = 0
    for element in remove_nodes:
        parent = parent_map.get(element)
        if parent is not None:
            parent.remove(element)
            removed += 1
    return removed


def scale_duration_value(value, factor):
    def replace(match):
        amount = float(match.group("number"))
        unit = match.group("unit")
        scaled = max(amount * factor, 0.01)
        formatted = f"{scaled:.3f}".rstrip("0").rstrip(".")
        return f"{formatted}{unit}"

    return DURATION_RE.sub(replace, value)


def scale_animation_speed(source, factor):
    if factor <= 0:
        raise ValueError("Animation speed factor must be greater than 0.")
    duration_factor = 1 / factor
    return re.sub(
        r"(?P<prefix>\b(?:dur|animation-duration)\s*[:=]\s*[\"']?)(?P<value>\d+(?:\.\d+)?(?:ms|s))",
        lambda match: match.group("prefix") + scale_duration_value(match.group("value"), duration_factor),
        source,
        flags=re.IGNORECASE,
    )


def serialize_svg(root):
    source = ET.tostring(root, encoding="unicode")
    return source if source.endswith("\n") else source + "\n"


def validate_svg_text(source):
    with tempfile.NamedTemporaryFile("w", suffix=".svg", encoding="utf-8", delete=False) as temp:
        temp.write(source)
        temp_path = Path(temp.name)
    try:
        return validate_svg(temp_path)
    finally:
        temp_path.unlink(missing_ok=True)


def apply_operations(source, operations):
    summary = {"colorsChanged": False, "textNodesChanged": 0, "elementsRemoved": 0, "animationScaled": False}
    if operations.get("replaceColors"):
        source = replace_colors(source, operations["replaceColors"])
        summary["colorsChanged"] = True
    if operations.get("scaleAnimationSpeed"):
        source = scale_animation_speed(source, float(operations["scaleAnimationSpeed"]))
        summary["animationScaled"] = True

    root = ET.fromstring(source)
    if operations.get("replaceText"):
        summary["textNodesChanged"] = replace_text(root, operations["replaceText"])
    if operations.get("removeElements"):
        summary["elementsRemoved"] = remove_elements(root, operations["removeElements"])

    output = serialize_svg(root)
    issues = validate_svg_text(output)
    if issues:
        raise ValueError("Edited SVG failed validation: " + "; ".join(issues))
    return output, summary


def capabilities_payload():
    operations = [
        {
            "id": "replaceColors",
            "label": "Replace Colors",
            "description": "Replace hex color tokens across SVG attributes and embedded style text.",
            "input": {"#2563eb": "#0f766e"},
        },
        {
            "id": "replaceText",
            "label": "Replace Text",
            "description": "Replace text nodes by edit id, element id, node path, or exact text.",
            "input": [{"target": "title", "to": "New title"}],
        },
        {
            "id": "removeElements",
            "label": "Remove Elements",
            "description": "Remove optional SVG elements by edit id, element id, or node path.",
            "input": ["decorative-orbit"],
        },
        {
            "id": "scaleAnimationSpeed",
            "label": "Scale Animation Speed",
            "description": "Scale animation timing while preserving safe SVG markup.",
            "input": 1.25,
        },
    ]
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "operationCount": len(operations),
        "operations": operations,
        "safety": {
            "validatesSvg": True,
            "blocksScripts": True,
            "blocksExternalReferences": True,
            "outputFormat": "svg",
        },
    }


def write_capabilities(output):
    payload = capabilities_payload()
    return write_json(output, payload), payload["operationCount"]


def check_capabilities(output):
    output = Path(output)
    expected = json.dumps(capabilities_payload(), indent=2, sort_keys=True) + "\n"
    if not output.exists():
        return "missing"
    if output.read_text(encoding="utf-8") != expected:
        return "changed"
    return None


def load_operations(value):
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


def run_self_tests():
    source = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40" role="img" aria-label="Demo"><title>Demo</title><text id="title" fill="#2563eb">Demo</text><circle id="dot" fill="#fff" r="2"/></svg>'
    output, summary = apply_operations(
        source,
        {
            "replaceColors": {"#2563eb": "#0f766e", "#fff": "#111827"},
            "replaceText": [{"target": "0.1", "to": "Updated"}],
            "removeElements": ["0.2"],
        },
    )
    assert "#0f766e" in output
    assert "Updated" in output
    assert "dot" not in output
    assert summary["textNodesChanged"] == 1
    assert capabilities_payload()["operationCount"] == 4
    print("svg_editor.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Safely edit SVG assets and generate editor capability metadata.")
    parser.add_argument("--input", help="Input SVG path.")
    parser.add_argument("--output", help="Output SVG path.")
    parser.add_argument("--operations", help="JSON string or JSON file with edit operations.")
    parser.add_argument("--capabilities-output", default="site/data/editor-capabilities.json", help="Editor capability JSON path relative to repo root.")
    parser.add_argument("--generate-capabilities", action="store_true", help="Write editor capability metadata.")
    parser.add_argument("--check", action="store_true", help="Verify editor capability metadata is current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused editor self-tests and exit.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    capabilities_output = root / args.capabilities_output
    if args.check:
        status = check_capabilities(capabilities_output)
        if status:
            print(f"::error file={rel_path(capabilities_output, root)}::Editor capabilities are {status}. Run npm run generate:editor-capabilities.")
            return 1
        print("Editor capabilities are current.")
        return 0

    if args.generate_capabilities:
        path, count = write_capabilities(capabilities_output)
        print(f"Wrote {count} editor operation(s) to {path}")
        return 0

    if not args.input or not args.output or not args.operations:
        parser.error("--input, --output, and --operations are required unless using --check, --self-test, or --generate-capabilities.")
    source = Path(args.input).read_text(encoding="utf-8")
    edited, summary = apply_operations(source, load_operations(args.operations))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(edited, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
