from pathlib import Path
import json
import re


EDITOR_DATA_SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/generators/generate_editor_data.py"
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


EDITOR_PRESETS = [
    {
        "id": "brand-swap",
        "name": "Brand Color Swap",
        "description": "Replace primary and secondary accent colors while leaving structure intact.",
        "operations": ["replaceColor"],
        "recommendedRoles": ["primaryAccent", "secondaryAccent", "glow"],
        "defaultPalette": "github-dark",
    },
    {
        "id": "readme-header-rebrand",
        "name": "README Header Rebrand",
        "description": "Update title text, accent colors, and optional decorative layers for header-style SVGs.",
        "operations": ["replaceColor", "replaceText", "hideElement"],
        "recommendedRoles": ["background", "surface", "primaryAccent", "text"],
        "defaultPalette": "readme-ux-kit",
    },
    {
        "id": "low-motion",
        "name": "Low Motion Variant",
        "description": "Slow animation timings and remove optional motion-heavy elements.",
        "operations": ["scaleAnimationSpeed", "hideElement"],
        "recommendedRoles": [],
        "defaultPalette": "github-light",
    },
    {
        "id": "status-tone",
        "name": "Status Tone",
        "description": "Map status colors for success, warning, danger, and neutral states.",
        "operations": ["replaceColor", "replaceText"],
        "recommendedRoles": ["success", "warning", "danger", "text"],
        "defaultPalette": "security-ops",
    },
    {
        "id": "docs-cleanup",
        "name": "Docs Cleanup",
        "description": "Convert highly stylized assets into lighter documentation-friendly colors.",
        "operations": ["replaceColor", "replaceText", "hideElement"],
        "recommendedRoles": ["background", "surface", "primaryAccent", "mutedText", "text"],
        "defaultPalette": "docs-clean",
    },
]


THEME_PALETTES = [
    {
        "id": "readme-ux-kit",
        "name": "README UX Kit",
        "roles": {
            "background": "#020617",
            "surface": "#0f172a",
            "primaryAccent": "#38bdf8",
            "secondaryAccent": "#a78bfa",
            "text": "#f8fafc",
            "mutedText": "#94a3b8",
            "stroke": "#334155",
            "glow": "#22d3ee",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "danger": "#ef4444",
        },
    },
    {
        "id": "github-dark",
        "name": "GitHub Dark",
        "roles": {
            "background": "#0d1117",
            "surface": "#161b22",
            "primaryAccent": "#58a6ff",
            "secondaryAccent": "#a5d6ff",
            "text": "#f0f6fc",
            "mutedText": "#8b949e",
            "stroke": "#30363d",
            "glow": "#1f6feb",
            "success": "#3fb950",
            "warning": "#d29922",
            "danger": "#f85149",
        },
    },
    {
        "id": "github-light",
        "name": "GitHub Light",
        "roles": {
            "background": "#ffffff",
            "surface": "#f6f8fa",
            "primaryAccent": "#0969da",
            "secondaryAccent": "#8250df",
            "text": "#24292f",
            "mutedText": "#57606a",
            "stroke": "#d0d7de",
            "glow": "#54aeff",
            "success": "#1a7f37",
            "warning": "#9a6700",
            "danger": "#cf222e",
        },
    },
    {
        "id": "neon",
        "name": "Neon",
        "roles": {
            "background": "#05070d",
            "surface": "#0b1020",
            "primaryAccent": "#22d3ee",
            "secondaryAccent": "#f472b6",
            "text": "#e5f4ff",
            "mutedText": "#94a3b8",
            "stroke": "#172033",
            "glow": "#8b5cf6",
            "success": "#34d399",
            "warning": "#fbbf24",
            "danger": "#fb365d",
        },
    },
    {
        "id": "enterprise",
        "name": "Enterprise",
        "roles": {
            "background": "#f8fafc",
            "surface": "#ffffff",
            "primaryAccent": "#2563eb",
            "secondaryAccent": "#4b5b73",
            "text": "#172033",
            "mutedText": "#64748b",
            "stroke": "#d7dee8",
            "glow": "#93c5fd",
            "success": "#16a34a",
            "warning": "#d97706",
            "danger": "#dc2626",
        },
    },
    {
        "id": "terminal",
        "name": "Terminal",
        "roles": {
            "background": "#020617",
            "surface": "#07111f",
            "primaryAccent": "#22c55e",
            "secondaryAccent": "#38bdf8",
            "text": "#e5e7eb",
            "mutedText": "#94a3b8",
            "stroke": "#1e293b",
            "glow": "#bbf7d0",
            "success": "#22c55e",
            "warning": "#facc15",
            "danger": "#fb7185",
        },
    },
    {
        "id": "data-lab",
        "name": "Data Lab",
        "roles": {
            "background": "#f8fafc",
            "surface": "#ffffff",
            "primaryAccent": "#0284c7",
            "secondaryAccent": "#7c3aed",
            "text": "#102033",
            "mutedText": "#475569",
            "stroke": "#dbeafe",
            "glow": "#0f766e",
            "success": "#0f766e",
            "warning": "#ca8a04",
            "danger": "#dc2626",
        },
    },
    {
        "id": "docs-clean",
        "name": "Docs Clean",
        "roles": {
            "background": "#ffffff",
            "surface": "#f9fafb",
            "primaryAccent": "#0f62fe",
            "secondaryAccent": "#7c3aed",
            "text": "#1f2937",
            "mutedText": "#667085",
            "stroke": "#e5e7eb",
            "glow": "#dbeafe",
            "success": "#2f855a",
            "warning": "#b7791f",
            "danger": "#c53030",
        },
    },
    {
        "id": "security-ops",
        "name": "Security Ops",
        "roles": {
            "background": "#0b1020",
            "surface": "#111827",
            "primaryAccent": "#38bdf8",
            "secondaryAccent": "#22c55e",
            "text": "#e5edf7",
            "mutedText": "#94a3b8",
            "stroke": "#334155",
            "glow": "#60a5fa",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "danger": "#ef4444",
        },
    },
]


def editor_presets_payload():
    return {
        "schemaVersion": EDITOR_DATA_SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "presets": EDITOR_PRESETS,
    }


def theme_palettes_payload():
    return {
        "schemaVersion": EDITOR_DATA_SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "palettes": THEME_PALETTES,
    }


def json_content(payload):
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def output_map(output_dir):
    return {
        "editor-presets.json": json_content(editor_presets_payload()),
        "theme-palettes.json": json_content(theme_palettes_payload()),
    }


def write_editor_data(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for filename, content in output_map(output_dir).items():
        path = output_dir / filename
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def validate_editor_presets(payload):
    errors = []
    if payload.get("schemaVersion") != EDITOR_DATA_SCHEMA_VERSION:
        errors.append("editor presets schemaVersion is invalid")
    preset_ids = set()
    palette_ids = {palette["id"] for palette in THEME_PALETTES}
    for index, preset in enumerate(payload.get("presets", [])):
        path = f"presets[{index}]"
        for key in ("id", "name", "description", "operations", "recommendedRoles", "defaultPalette"):
            if key not in preset:
                errors.append(f"{path}.{key} is required")
        if preset.get("id") in preset_ids:
            errors.append(f"{path}.id must be unique")
        preset_ids.add(preset.get("id"))
        unknown_operations = set(preset.get("operations", [])) - {"replaceColor", "replaceText", "hideElement", "scaleAnimationSpeed"}
        if unknown_operations:
            errors.append(f"{path}.operations has unknown values: {', '.join(sorted(unknown_operations))}")
        if preset.get("defaultPalette") not in palette_ids:
            errors.append(f"{path}.defaultPalette must reference a known palette")
    return errors


def validate_theme_palettes(payload):
    errors = []
    if payload.get("schemaVersion") != EDITOR_DATA_SCHEMA_VERSION:
        errors.append("theme palettes schemaVersion is invalid")
    palette_ids = set()
    required_roles = {"background", "surface", "primaryAccent", "secondaryAccent", "text", "mutedText", "stroke"}
    for index, palette in enumerate(payload.get("palettes", [])):
        path = f"palettes[{index}]"
        for key in ("id", "name", "roles"):
            if key not in palette:
                errors.append(f"{path}.{key} is required")
        if palette.get("id") in palette_ids:
            errors.append(f"{path}.id must be unique")
        palette_ids.add(palette.get("id"))
        roles = palette.get("roles", {})
        missing_roles = sorted(required_roles - set(roles))
        if missing_roles:
            errors.append(f"{path}.roles missing required roles: {', '.join(missing_roles)}")
        for role, value in roles.items():
            if not isinstance(value, str) or not HEX_RE.match(value):
                errors.append(f"{path}.roles.{role} must be a 6-digit hex color")
    return errors


def validate_output_payload(filename, payload):
    if filename == "editor-presets.json":
        return validate_editor_presets(payload)
    if filename == "theme-palettes.json":
        return validate_theme_palettes(payload)
    return [f"unknown editor data file: {filename}"]


def check_editor_data(output_dir):
    failures = []
    for filename, expected in output_map(output_dir).items():
        path = output_dir / filename
        if not path.exists():
            failures.append((path, "missing", []))
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            failures.append((path, "changed", []))
            continue
        try:
            payload = json.loads(actual)
        except json.JSONDecodeError as error:
            failures.append((path, "invalid-json", [str(error)]))
            continue
        errors = validate_output_payload(filename, payload)
        if errors:
            failures.append((path, "invalid", errors))
    return failures


def print_check_failures(failures):
    print("Editor data is stale or invalid. Regenerate it with:")
    print()
    print("  python src/modules/generators/generate_editor_data.py")
    print()
    for path, status, errors in failures[:20]:
        print(f"::error file={path.as_posix()}::Editor data is {status}: {path.as_posix()}")
        for error in errors[:10]:
            print(f"::error file={path.as_posix()}::{error}")


def run_self_tests():
    presets = editor_presets_payload()
    palettes = theme_palettes_payload()
    assert validate_editor_presets(presets) == []
    assert validate_theme_palettes(palettes) == []
    assert len(presets["presets"]) >= 5
    assert len(palettes["palettes"]) >= 6
    assert any(preset["id"] == "brand-swap" for preset in presets["presets"])
    assert any(palette["id"] == "github-dark" for palette in palettes["palettes"])
    print("editor_presets.py self-tests passed.")


__all__ = [
    "check_editor_data",
    "editor_presets_payload",
    "print_check_failures",
    "run_self_tests",
    "theme_palettes_payload",
    "write_editor_data",
]
