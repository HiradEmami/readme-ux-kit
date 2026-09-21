from pathlib import Path
import argparse
import json
import re
import tempfile

from src.modules.common.repo import load_json, natural_title, read_text, rel_path, repo_root, strip_fenced_blocks, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/indexers/template_index.py"
VALID_MATURITIES = {"stable", "draft", "experimental"}
DEFAULT_OPTIONAL_SECTIONS = ("repository-map", "configuration", "support", "roadmap", "security", "architecture")
DEFAULT_ASSET_CATEGORIES = ("headers", "dividers", "icons")
REQUIRED_CONTRACT_FIELDS = (
    "id",
    "title",
    "maturity",
    "bestFor",
    "requiredMetadata",
    "optionalMetadata",
    "requiredSections",
    "optionalSections",
    "recommendedComponents",
    "compatibleThemes",
    "recommendedAssetCategories",
    "requiredPlaceholders",
    "placeholderDefaults",
    "qualityChecks",
    "sectionsToRemoveWhenNotRelevant",
)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def template_files(root):
    return sorted(
        [path for path in (Path(root) / "templates").glob("*.md") if path.name != "README.md"],
        key=lambda path: path.name.lower(),
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


def read_contract(root, template_id):
    path = Path(root) / "templates" / "contracts" / f"{template_id}.json"
    if not path.exists():
        return {}
    return load_json(path)


def maturity_from_metadata(metadata, contract, path):
    values = code_values(metadata.get("maturity", ""))
    maturity = values[0] if values else metadata.get("maturity", "").strip("` ")
    if maturity in VALID_MATURITIES:
        return maturity
    if contract.get("maturity") in VALID_MATURITIES:
        return contract["maturity"]
    if "Copy Checklist" in read_text(path):
        return "stable"
    return "draft"


def template_record(root, path):
    template_id = path.stem
    metadata = metadata_lines(path)
    contract = read_contract(root, template_id)
    required_placeholders = contract.get("requiredPlaceholders") or ("PROJECT_NAME", "INSTALL_COMMAND", "RUN_COMMAND", "TEST_COMMAND")
    return {
        "id": template_id,
        "title": contract.get("title") or title_from_markdown(path),
        "path": rel_path(path, root),
        "contract": f"templates/contracts/{template_id}.json",
        "maturity": maturity_from_metadata(metadata, contract, path),
        "bestFor": contract.get("bestFor") or metadata.get("best for") or first_plain_paragraph(path),
        "supportedProjectTypes": contract.get("supportedProjectTypes") or [template_id],
        "compatibleThemes": contract.get("compatibleThemes") or code_values(metadata.get("compatible themes", "")),
        "recommendedComponents": contract.get("recommendedComponents") or [],
        "requiredPlaceholders": list(required_placeholders),
        "optionalSections": contract.get("optionalSections") or list(DEFAULT_OPTIONAL_SECTIONS),
        "outputDensity": contract.get("outputDensity", "medium"),
    }


def build_template_index(root=None):
    root = Path(root or repo_root()).resolve()
    templates = [template_record(root, path) for path in template_files(root)]
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "templateCount": len(templates),
        "templates": templates,
    }


def known_component_ids(root):
    return {f"{path.parent.name}/{path.stem}" for path in (Path(root) / "components").rglob("*.md") if path.name != "README.md"}


def known_theme_ids(root):
    return {path.name for path in (Path(root) / "themes").iterdir() if path.is_dir()}


def validate_contract(root, template_id, payload):
    errors = []
    if not payload:
        return [f"templates/contracts/{template_id}.json is missing."]
    for field in REQUIRED_CONTRACT_FIELDS:
        if field not in payload:
            errors.append(f"templates/contracts/{template_id}.json is missing {field}.")
    if payload.get("id") != template_id:
        errors.append(f"templates/contracts/{template_id}.json id does not match template file.")
    if payload.get("maturity") not in VALID_MATURITIES:
        errors.append(f"templates/contracts/{template_id}.json has invalid maturity: {payload.get('maturity')}")
    for placeholder in payload.get("requiredPlaceholders", []) + payload.get("requiredMetadata", []) + payload.get("optionalMetadata", []):
        if not PLACEHOLDER_RE.match(placeholder):
            errors.append(f"templates/contracts/{template_id}.json has invalid placeholder {placeholder}.")
    for placeholder in payload.get("placeholderDefaults", {}):
        if not PLACEHOLDER_RE.match(placeholder):
            errors.append(f"templates/contracts/{template_id}.json has invalid placeholder default key {placeholder}.")
    return errors


def validation_errors(payload, root=None):
    root = Path(root or repo_root()).resolve()
    errors = []
    indexed_paths = set()
    component_ids = known_component_ids(root)
    theme_ids = known_theme_ids(root)
    for template in payload.get("templates", []):
        path = root / template.get("path", "")
        if not path.exists():
            errors.append(f"{template.get('id', '<unknown>')} references missing file: {template.get('path')}")
        else:
            indexed_paths.add(rel_path(path, root))
            if template.get("maturity") == "stable" and "## Copy Checklist" not in read_text(path):
                errors.append(f"{template['id']} is stable but has no Copy Checklist section.")
        contract_path = root / template.get("contract", "")
        contract = {}
        if contract_path.exists():
            try:
                contract = load_json(contract_path)
            except json.JSONDecodeError as error:
                errors.append(f"{rel_path(contract_path, root)} is invalid JSON: {error}")
        errors.extend(validate_contract(root, template.get("id", ""), contract))
        for component in template.get("recommendedComponents", []):
            if component not in component_ids:
                errors.append(f"{template.get('id', '<unknown>')} references unknown component: {component}")
        for theme in template.get("compatibleThemes", []):
            if theme not in theme_ids:
                errors.append(f"{template.get('id', '<unknown>')} references unknown theme: {theme}")
        for placeholder in template.get("requiredPlaceholders", []):
            if not PLACEHOLDER_RE.match(placeholder):
                errors.append(f"{template.get('id', '<unknown>')} has invalid placeholder {placeholder}.")
    for path in template_files(root):
        relative = rel_path(path, root)
        if relative not in indexed_paths:
            errors.append(f"{relative} is not represented in templates/index.json.")
    if payload.get("templateCount") != len(payload.get("templates", [])):
        errors.append("templateCount does not match templates length.")
    return errors


def write_template_index(output=None, root=None):
    root = Path(root or repo_root()).resolve()
    output = Path(output or root / "templates" / "index.json")
    payload = build_template_index(root)
    return write_json(output, payload), payload["templateCount"]


def check_template_index(output=None, root=None):
    root = Path(root or repo_root()).resolve()
    output = Path(output or root / "templates" / "index.json")
    payload = build_template_index(root)
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
        (root / "templates" / "contracts").mkdir(parents=True)
        (root / "components" / "navigation").mkdir(parents=True)
        (root / "themes" / "minimal").mkdir(parents=True)
        (root / "components" / "navigation" / "start-here.md").write_text("# Start Here\n", encoding="utf-8")
        (root / "templates" / "minimal.md").write_text("# PROJECT_NAME\n\n> Maturity: `stable`\n\n## Copy Checklist\n\n- [ ] Replace placeholders.\n", encoding="utf-8")
        (root / "templates" / "contracts" / "minimal.json").write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "id": "minimal",
                    "title": "Minimal",
                    "maturity": "stable",
                    "bestFor": "Small tools",
                    "requiredMetadata": ["PROJECT_NAME"],
                    "optionalMetadata": ["OWNER", "REPO"],
                    "requiredSections": ["overview"],
                    "optionalSections": ["support"],
                    "recommendedComponents": ["navigation/start-here"],
                    "compatibleThemes": ["minimal"],
                    "recommendedAssetCategories": ["headers"],
                    "requiredPlaceholders": ["PROJECT_NAME"],
                    "placeholderDefaults": {"INSTALL_COMMAND": "npm install"},
                    "qualityChecks": ["replace-placeholders"],
                    "sectionsToRemoveWhenNotRelevant": ["support"],
                }
            ),
            encoding="utf-8",
        )
        payload = build_template_index(root)
        assert payload["templateCount"] == 1
        assert validation_errors(payload, root) == []
    print("template_index.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate and validate the template index.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="templates/index.json", help="Template index path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify the template index without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused template index self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    if args.check:
        status, errors = check_template_index(output, root)
        if status:
            print(f"::error file={rel_path(output, root)}::Template index is {status}. Run npm run generate:templates.")
        for error in errors:
            print(f"::error::{error}")
        if status or errors:
            return 1
        print("Template index is current.")
        return 0

    path, count = write_template_index(output, root)
    print(f"Wrote {count} template record(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
