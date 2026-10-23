from pathlib import Path
import argparse
import json
import re
import tempfile

from src.modules.common.repo import natural_title, read_text, rel_path, repo_root, strip_fenced_blocks, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/indexers/component_index.py"
DEFAULT_COMPATIBLE_TEMPLATES = ("minimal", "open-source-lib", "backend-service")
DEFAULT_COMPATIBLE_THEMES = ("minimal", "docs-clean", "enterprise", "open-source-classic")
VALID_MATURITIES = {"stable", "draft", "experimental"}
REQUIRED_FIELDS = (
    "id",
    "title",
    "group",
    "path",
    "maturity",
    "bestFor",
    "compatibleTemplates",
    "compatibleThemes",
    "requiredPlaceholders",
    "optionalPlaceholders",
    "githubCompatibility",
)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def component_files(root):
    root = Path(root)
    return sorted(
        [path for path in (root / "components").rglob("*.md") if path.name != "README.md"],
        key=lambda path: path.as_posix().lower(),
    )


def title_from_markdown(path):
    match = HEADING_RE.search(read_text(path))
    return match.group(1).strip() if match else natural_title(path)


def metadata_lines(path):
    metadata = {}
    for line in read_text(path).splitlines()[:16]:
        if not line.startswith(">") or ":" not in line:
            continue
        key, value = line.lstrip("> ").split(":", 1)
        metadata[key.strip().lower()] = value.strip()
    return metadata


def first_plain_paragraph(path):
    text = strip_fenced_blocks(read_text(path))
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ">", "|", "-", "<")):
            continue
        return line
    return ""


def code_values(value):
    found = INLINE_CODE_RE.findall(value)
    return [item.strip() for item in found if item.strip()]


def section_values(path, heading):
    text = strip_fenced_blocks(read_text(path))
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        return []
    values = []
    for line in match.group("body").splitlines():
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        codes = code_values(stripped)
        values.extend(codes or [stripped.lstrip("- ").strip()])
    return sorted(set(value for value in values if value))


def maturity_from_metadata(metadata, path):
    maturity = (code_values(metadata.get("maturity", "")) or [metadata.get("maturity", "").strip("` ")])[0]
    if maturity in VALID_MATURITIES:
        return maturity
    if "Copy Checklist" in read_text(path):
        return "stable"
    return "draft"


def component_record(root, path):
    relative = rel_path(path, root)
    metadata = metadata_lines(path)
    group = path.parent.name
    best_for = metadata.get("best for") or first_plain_paragraph(path) or f"{natural_title(path)} README section."
    compatible_templates = code_values(metadata.get("compatible templates", "")) or list(DEFAULT_COMPATIBLE_TEMPLATES)
    compatible_themes = code_values(metadata.get("compatible themes", "")) or list(DEFAULT_COMPATIBLE_THEMES)
    return {
        "id": f"{group}/{path.stem}",
        "title": title_from_markdown(path),
        "group": group,
        "path": relative,
        "maturity": maturity_from_metadata(metadata, path),
        "bestFor": best_for.rstrip(".") + ".",
        "compatibleTemplates": compatible_templates,
        "compatibleThemes": compatible_themes,
        "requiredPlaceholders": section_values(path, "Required Placeholders"),
        "optionalPlaceholders": section_values(path, "Optional Placeholders"),
        "githubCompatibility": "Standard GitHub Markdown tables, lists, links, and code spans.",
        "motionLevel": "varies" if "animated" in read_text(path).lower() else "none",
    }


def build_component_index(root=None):
    root = Path(root or repo_root()).resolve()
    components = [component_record(root, path) for path in component_files(root)]
    groups = []
    for group in sorted({item["group"] for item in components}):
        groups.append(
            {
                "id": group,
                "path": f"components/{group}/",
                "purpose": f"{natural_title(group)} README components.",
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "componentCount": len(components),
        "groups": groups,
        "components": components,
    }


def known_template_ids(root):
    return {path.stem for path in (Path(root) / "templates").glob("*.md") if path.name != "README.md"}


def known_theme_ids(root):
    return {path.name for path in (Path(root) / "themes").iterdir() if path.is_dir()}


def validation_errors(payload, root=None):
    root = Path(root or repo_root()).resolve()
    errors = []
    indexed_paths = set()
    template_ids = known_template_ids(root)
    theme_ids = known_theme_ids(root)
    for component in payload.get("components", []):
        for field in REQUIRED_FIELDS:
            if field not in component:
                errors.append(f"{component.get('id', '<unknown>')} is missing {field}.")
        path = root / component.get("path", "")
        if not path.exists():
            errors.append(f"{component.get('id', '<unknown>')} references missing file: {component.get('path')}")
        else:
            indexed_paths.add(rel_path(path, root))
            text = read_text(path)
            if component.get("maturity") == "stable" and "## Copy Checklist" not in text:
                errors.append(f"{component['id']} is stable but has no Copy Checklist section.")
        if component.get("maturity") not in VALID_MATURITIES:
            errors.append(f"{component.get('id', '<unknown>')} has invalid maturity: {component.get('maturity')}")
        for field in ("requiredPlaceholders", "optionalPlaceholders"):
            for placeholder in component.get(field, []):
                if not PLACEHOLDER_RE.match(placeholder):
                    errors.append(f"{component.get('id', '<unknown>')} has invalid placeholder {placeholder}.")
        for template in component.get("compatibleTemplates", []):
            if template not in template_ids:
                errors.append(f"{component.get('id', '<unknown>')} references unknown template: {template}")
        for theme in component.get("compatibleThemes", []):
            if theme not in theme_ids:
                errors.append(f"{component.get('id', '<unknown>')} references unknown theme: {theme}")
    for path in component_files(root):
        relative = rel_path(path, root)
        if relative not in indexed_paths:
            errors.append(f"{relative} is not represented in components/index.json.")
    if payload.get("componentCount") != len(payload.get("components", [])):
        errors.append("componentCount does not match components length.")
    return errors


def write_component_index(output=None, root=None):
    root = Path(root or repo_root()).resolve()
    output = Path(output or root / "components" / "index.json")
    payload = build_component_index(root)
    return write_json(output, payload), payload["componentCount"]


def check_component_index(output=None, root=None):
    root = Path(root or repo_root()).resolve()
    output = Path(output or root / "components" / "index.json")
    payload = build_component_index(root)
    expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    status = None
    if not output.exists():
        status = "missing"
    elif output.read_text(encoding="utf-8") != expected:
        status = "changed"
    return status, validation_errors(payload, root)


def run_self_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "components" / "navigation").mkdir(parents=True)
        (root / "templates").mkdir()
        (root / "themes" / "minimal").mkdir(parents=True)
        (root / "templates" / "minimal.md").write_text("# Minimal\n", encoding="utf-8")
        (root / "components" / "navigation" / "start-here.md").write_text(
            "# Start Here\n\n"
            "> Maturity: `stable`\n"
            "> Best for: Reader routing.\n"
            "> Compatible themes: `minimal`\n"
            "> Compatible templates: `minimal`\n\n"
            "## Required Placeholders\n\n- `PROJECT_NAME`\n\n"
            "## Copy Checklist\n\n- [ ] Replace placeholders.\n",
            encoding="utf-8",
        )
        payload = build_component_index(root)
        assert payload["componentCount"] == 1
        assert validation_errors(payload, root) == []
    print("component_index.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate and validate the component index.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="components/index.json", help="Component index path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify the component index without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused component index self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    if args.check:
        status, errors = check_component_index(output, root)
        if status:
            print(f"::error file={rel_path(output, root)}::Component index is {status}. Run npm run generate:components.")
        for error in errors:
            print(f"::error::{error}")
        if status or errors:
            return 1
        print("Component index is current.")
        return 0

    path, count = write_component_index(output, root)
    print(f"Wrote {count} component record(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
