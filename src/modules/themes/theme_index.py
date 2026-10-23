from pathlib import Path
import argparse
import json
import re
import tempfile

from src.modules.common.repo import load_json, markdown_links, natural_title, read_text, rel_path, repo_root, split_link_target, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/themes/theme_index.py"
EXPECTED_THEME_FILES = (
    "example.md",
    "colors.md",
    "assets-map.md",
    "tokens.json",
    "usage.md",
    "voice.md",
    "components.md",
    "template-matrix.md",
    "contrast.md",
    "preview.md",
)
THEME_PATH_KEYS = {
    "example.md": "example",
    "colors.md": "colors",
    "assets-map.md": "assetsMap",
    "tokens.json": "tokens",
    "usage.md": "usage",
    "voice.md": "voice",
    "components.md": "components",
    "template-matrix.md": "templateMatrix",
    "contrast.md": "contrast",
    "preview.md": "preview",
}
THEME_ROW_RE = re.compile(r"^\|\s*\[([^\]]+)\]\(\./([^/]+)/example\.md\)\s*\|\s*([^|]+)\|\s*([^|]+)\|")
HEX_RE = re.compile(r"`?(#[0-9a-fA-F]{6})`?")
STRICT_HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
WORD_RE = re.compile(r"[a-z0-9]+")


def slug_tokens(*values):
    tokens = set()
    for value in values:
        tokens.update(WORD_RE.findall(str(value).lower()))
    return sorted(tokens)


def parse_theme_readme(root):
    path = root / "themes" / "README.md"
    if not path.exists():
        return {}
    themes = {}
    for line in read_text(path).splitlines():
        match = THEME_ROW_RE.match(line.strip())
        if match:
            name, theme_id, best_for, summary = match.groups()
            themes[theme_id] = {
                "name": name.strip(),
                "bestFor": best_for.strip(),
                "summary": summary.strip().rstrip("."),
            }
    return themes


def first_paragraph(path):
    if not path.exists():
        return ""
    for line in read_text(path).splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("|") and not line.startswith("["):
            return line.lstrip("> ").strip()
    return ""


def parse_colors(path):
    colors = []
    if not path.exists():
        return colors
    for line in read_text(path).splitlines():
        if not line.strip().startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "token":
            continue
        match = HEX_RE.search(cells[1])
        if match:
            colors.append({"token": cells[0], "hex": match.group(1).lower(), "use": cells[2]})
    return colors


def parse_asset_map(root, path):
    assets = []
    if not path.exists():
        return assets
    for line in read_text(path).splitlines():
        if not line.strip().startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "section":
            continue
        links = markdown_links_from_text(cells[1])
        if not links:
            continue
        path_text, _ = split_link_target(links[0])
        target = (path.parent / path_text).resolve()
        assets.append(
            {
                "section": cells[0],
                "label": re.sub(r"`|\[|\]|\([^)]*\)", "", cells[1]).strip(),
                "path": rel_path(target, root) if target.exists() else path_text,
                "purpose": cells[2],
                "exists": target.exists(),
            }
        )
    return assets


def parse_theme_tokens(root, path):
    if not path.exists():
        return {}, []
    try:
        payload = load_json(path)
    except json.JSONDecodeError as error:
        return {}, [f"{rel_path(path, root)} is invalid JSON: {error}"]

    errors = []
    colors = []
    for item in payload.get("colors", []):
        hex_value = str(item.get("hex", "")).lower()
        colors.append({"token": item.get("token", ""), "hex": hex_value, "use": item.get("use", "")})
        if not STRICT_HEX_RE.match(hex_value):
            errors.append(f"{rel_path(path, root)} has invalid color: {hex_value}")

    assets = []
    for item in payload.get("assets", []):
        asset_path = str(item.get("path", ""))
        exists = bool(asset_path) and (root / asset_path).exists()
        assets.append(
            {
                "section": item.get("section", ""),
                "label": Path(asset_path).name,
                "path": asset_path,
                "purpose": item.get("purpose", ""),
                "exists": exists,
            }
        )
        if not exists:
            errors.append(f"{rel_path(path, root)} references missing asset: {asset_path}")
    return {**payload, "colors": colors, "assets": assets}, errors


def markdown_links_from_text(text):
    return re.findall(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text)


def theme_status(theme_dir, colors, assets, token_errors):
    missing = [name for name in EXPECTED_THEME_FILES if not (theme_dir / name).exists()]
    warnings = []
    if len(colors) < 4:
        warnings.append("few-colors")
    if len(assets) < 4:
        warnings.append("few-assets")
    if any(not asset["exists"] for asset in assets) or token_errors:
        missing.append("asset-map-links")
    return {"complete": not missing, "missing": missing, "warnings": warnings}


def build_theme_index(root=None):
    root = Path(root or repo_root()).resolve()
    readme_metadata = parse_theme_readme(root)
    themes = []
    themes_root = root / "themes"
    for theme_dir in sorted([item for item in themes_root.iterdir() if item.is_dir()], key=lambda path: path.name.lower()):
        metadata = readme_metadata.get(theme_dir.name, {})
        token_payload, token_errors = parse_theme_tokens(root, theme_dir / "tokens.json")
        colors = token_payload.get("colors") or parse_colors(theme_dir / "colors.md")
        assets = parse_asset_map(root, theme_dir / "assets-map.md") or token_payload.get("assets", [])
        summary = metadata.get("summary") or token_payload.get("feel") or first_paragraph(theme_dir / "example.md")
        name = token_payload.get("name") or metadata.get("name") or natural_title(theme_dir)
        best_for = token_payload.get("bestFor") or metadata.get("bestFor", "")
        paths = {THEME_PATH_KEYS[name_]: rel_path(theme_dir / name_, root) for name_ in EXPECTED_THEME_FILES if (theme_dir / name_).exists()}
        themes.append(
            {
                "id": theme_dir.name,
                "name": name,
                "bestFor": best_for,
                "summary": summary,
                "tone": token_payload.get("tone", ""),
                "density": token_payload.get("density", ""),
                "motionLevel": token_payload.get("motionLevel", ""),
                "assetStrategy": token_payload.get("assetStrategy", ""),
                "recommendedComponents": token_payload.get("recommendedComponents", []),
                "recommendedTemplates": token_payload.get("recommendedTemplates", {}),
                "tags": slug_tokens(theme_dir.name, name, best_for, summary),
                "paths": paths,
                "colors": colors,
                "assets": assets,
                "status": theme_status(theme_dir, colors, assets, token_errors),
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "themeCount": len(themes),
        "themes": themes,
    }


def validation_errors(payload, root=None):
    root = Path(root or repo_root()).resolve()
    template_ids = {path.stem for path in (root / "templates").glob("*.md") if path.name != "README.md"}
    component_ids = {f"{path.parent.name}/{path.stem}" for path in (root / "components").rglob("*.md") if path.name != "README.md"}
    errors = []
    for theme in payload["themes"]:
        if not theme["status"]["complete"]:
            errors.append(f"{theme['id']} is incomplete: {', '.join(theme['status']['missing'])}")
        if theme.get("motionLevel") not in {"none", "low", "medium", "moderate", "high", ""}:
            errors.append(f"{theme['id']} has invalid motionLevel: {theme.get('motionLevel')}")
        for component in theme.get("recommendedComponents", []):
            if component not in component_ids:
                errors.append(f"{theme['id']} references unknown component: {component}")
        for fit, templates in theme.get("recommendedTemplates", {}).items():
            if fit == "poor":
                continue
            for template in templates:
                if template not in template_ids:
                    errors.append(f"{theme['id']} references unknown {fit} template: {template}")
        for color in theme["colors"]:
            if not STRICT_HEX_RE.match(color.get("hex", "")):
                errors.append(f"{theme['id']} has invalid color: {color.get('hex')}")
        for asset in theme["assets"]:
            if not asset["exists"]:
                errors.append(f"{theme['id']} references missing asset: {asset['path']}")
    return errors


def write_theme_indexes(theme_output, site_output, root=None):
    payload = build_theme_index(root)
    return [write_json(theme_output, payload), write_json(site_output, payload)], payload["themeCount"]


def check_theme_indexes(theme_output, site_output, root=None):
    payload = build_theme_index(root)
    expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    failures = []
    for path in [Path(theme_output), Path(site_output)]:
        if not path.exists():
            failures.append((path, "missing"))
        elif path.read_text(encoding="utf-8") != expected:
            failures.append((path, "changed"))
    return failures, validation_errors(payload, root)


def run_self_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "themes" / "demo").mkdir(parents=True)
        (root / "components" / "navigation").mkdir(parents=True)
        (root / "templates").mkdir()
        (root / "assets").mkdir()
        (root / "assets" / "demo.svg").write_text("<svg/>", encoding="utf-8")
        (root / "components" / "navigation" / "start-here.md").write_text("# Start Here\n", encoding="utf-8")
        (root / "templates" / "minimal.md").write_text("# Minimal\n", encoding="utf-8")
        (root / "themes" / "README.md").write_text(
            "# Themes\n\n| Theme | Best for | Direction |\n| --- | --- | --- |\n| [Demo](./demo/example.md) | Tests | Clean. |\n",
            encoding="utf-8",
        )
        (root / "themes" / "demo" / "example.md").write_text("# Demo\n\n> Clean demo.\n", encoding="utf-8")
        (root / "themes" / "demo" / "colors.md").write_text(
            "# Colors\n\n| Token | Hex | Use |\n| --- | --- | --- |\n| Ink | `#111827` | Text |\n| Blue | `#2563eb` | Links |\n| Line | `#cbd5e1` | Rules |\n| Mist | `#f8fafc` | Background |\n",
            encoding="utf-8",
        )
        (root / "themes" / "demo" / "assets-map.md").write_text(
            "# Asset Map\n\n| Section | Asset | Purpose |\n| --- | --- | --- |\n| Hero | [`demo.svg`](../../assets/demo.svg) | Testing |\n| Icon | [`demo.svg`](../../assets/demo.svg) | Testing |\n| Divider | [`demo.svg`](../../assets/demo.svg) | Testing |\n| Footer | [`demo.svg`](../../assets/demo.svg) | Testing |\n",
            encoding="utf-8",
        )
        (root / "themes" / "demo" / "tokens.json").write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "id": "demo",
                    "name": "Demo",
                    "bestFor": "Tests",
                    "feel": "Clean",
                    "tone": "Direct",
                    "density": "compact",
                    "motionLevel": "low",
                    "assetStrategy": "Use one asset.",
                    "recommendedComponents": ["navigation/start-here"],
                    "recommendedTemplates": {"excellent": ["minimal"], "acceptable": [], "poor": []},
                    "colors": [
                        {"token": "Ink", "hex": "#111827", "use": "Text"},
                        {"token": "Blue", "hex": "#2563eb", "use": "Links"},
                        {"token": "Line", "hex": "#cbd5e1", "use": "Rules"},
                        {"token": "Mist", "hex": "#f8fafc", "use": "Background"},
                    ],
                    "assets": [{"section": "Hero", "path": "assets/demo.svg", "purpose": "Testing"}],
                }
            ),
            encoding="utf-8",
        )
        for name in ("usage.md", "voice.md", "components.md", "template-matrix.md", "contrast.md", "preview.md"):
            (root / "themes" / "demo" / name).write_text("# Demo\n", encoding="utf-8")
        payload = build_theme_index(root)
        assert payload["themeCount"] == 1
        assert validation_errors(payload, root) == []
    print("theme_index.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate and validate the theme registry.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="themes/index.json", help="Theme index path relative to repo root.")
    parser.add_argument("--site-output", default="site/data/themes.json", help="Site theme data path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify generated theme indexes and theme docs without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused theme self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    site_output = root / args.site_output
    if args.check:
        failures, errors = check_theme_indexes(output, site_output, root)
        for path, status in failures:
            print(f"::error file={rel_path(path, root)}::Theme index is {status}. Run npm run generate:themes.")
        for error in errors:
            print(f"::error::{error}")
        if failures or errors:
            return 1
        print("Theme indexes and docs are current.")
        return 0

    paths, count = write_theme_indexes(output, site_output, root)
    for path in paths:
        print(f"Wrote {count} theme record(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
