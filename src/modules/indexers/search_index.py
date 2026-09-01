from pathlib import Path
import argparse
import json
import re

from src.modules.common.repo import load_json, natural_title, read_text, rel_path, repo_root, strip_fenced_blocks, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/indexers/search_index.py"
WORD_RE = re.compile(r"[a-z0-9]+")
HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)


def tokens_for(*values):
    tokens = set()
    for value in values:
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            tokens.update(tokens_for(*value))
        else:
            tokens.update(WORD_RE.findall(str(value).lower()))
    return sorted(tokens)


def markdown_summary(path):
    text = strip_fenced_blocks(read_text(path))
    lines = [line.strip() for line in text.splitlines()]
    title = natural_title(path)
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    paragraphs = [line for line in lines if line and not line.startswith("#") and not line.startswith("|") and not line.startswith("-")]
    return {
        "title": title,
        "summary": paragraphs[0] if paragraphs else "",
        "headings": [heading.strip() for heading in HEADING_RE.findall(text)[:12]],
    }


def asset_entries(manifest):
    entries = []
    for asset in manifest["assets"]:
        entries.append(
            {
                "id": f"asset:{asset['path']}",
                "kind": "asset",
                "title": asset["name"],
                "path": asset["path"],
                "url": asset["previewPath"],
                "category": asset["category"],
                "subcategory": asset["subcategory"],
                "tags": asset["tags"],
                "tokens": tokens_for(asset["name"], asset["category"], asset["subcategory"], asset["tags"], asset.get("editorQuality")),
            }
        )
    return entries


def template_entries(root):
    entries = []
    for path in sorted((root / "templates").glob("*.md"), key=lambda item: item.name.lower()):
        if path.name == "README.md":
            continue
        info = markdown_summary(path)
        entries.append(
            {
                "id": f"template:{rel_path(path, root)}",
                "kind": "template",
                "title": info["title"],
                "path": rel_path(path, root),
                "summary": info["summary"],
                "headings": info["headings"],
                "tags": tokens_for(path.stem, info["title"]),
                "tokens": tokens_for(path.stem, info["title"], info["summary"], info["headings"]),
            }
        )
    return entries


def component_entries(root):
    entries = []
    for path in sorted((root / "components").rglob("*.md"), key=lambda item: item.as_posix().lower()):
        if path.name == "README.md":
            continue
        info = markdown_summary(path)
        group = path.parent.name
        entries.append(
            {
                "id": f"component:{rel_path(path, root)}",
                "kind": "component",
                "title": info["title"],
                "path": rel_path(path, root),
                "group": group,
                "summary": info["summary"],
                "headings": info["headings"],
                "tags": tokens_for(group, path.stem, info["title"]),
                "tokens": tokens_for(group, path.stem, info["title"], info["summary"], info["headings"]),
            }
        )
    return entries


def theme_entries(root):
    theme_index = root / "themes" / "index.json"
    if theme_index.exists():
        themes = load_json(theme_index)["themes"]
        return [
            {
                "id": f"theme:{theme['id']}",
                "kind": "theme",
                "title": theme["name"],
                "path": theme["paths"]["example"],
                "summary": theme.get("summary", ""),
                "tags": theme.get("tags", []),
                "tokens": tokens_for(theme["id"], theme["name"], theme.get("summary", ""), theme.get("tags", [])),
            }
            for theme in themes
        ]

    entries = []
    for theme_dir in sorted((root / "themes").iterdir(), key=lambda item: item.name.lower()):
        if not theme_dir.is_dir():
            continue
        example = theme_dir / "example.md"
        if not example.exists():
            continue
        info = markdown_summary(example)
        entries.append(
            {
                "id": f"theme:{theme_dir.name}",
                "kind": "theme",
                "title": info["title"],
                "path": rel_path(example, root),
                "summary": info["summary"],
                "tags": tokens_for(theme_dir.name, info["title"]),
                "tokens": tokens_for(theme_dir.name, info["title"], info["summary"], info["headings"]),
            }
        )
    return entries


def tag_index(entries):
    tags = {}
    for entry in entries:
        for tag in entry.get("tags", []):
            tags.setdefault(tag, {"tag": tag, "count": 0, "kinds": {}})
            tags[tag]["count"] += 1
            tags[tag]["kinds"][entry["kind"]] = tags[tag]["kinds"].get(entry["kind"], 0) + 1
    return [
        {"tag": tag, "count": data["count"], "kinds": dict(sorted(data["kinds"].items()))}
        for tag, data in sorted(tags.items())
    ]


def build_indexes(root=None, manifest_path=None):
    root = Path(root or repo_root()).resolve()
    manifest = load_json(manifest_path or root / "assets" / "manifest.json")
    assets = asset_entries(manifest)
    templates = template_entries(root)
    components = component_entries(root)
    themes = theme_entries(root)
    search = assets + templates + components + themes
    return {
        "search-index.json": {
            "schemaVersion": SCHEMA_VERSION,
            "generatedBy": GENERATOR_NAME,
            "entryCount": len(search),
            "entries": sorted(search, key=lambda item: (item["kind"], item["path"])),
        },
        "templates.json": {
            "schemaVersion": SCHEMA_VERSION,
            "generatedBy": GENERATOR_NAME,
            "templateCount": len(templates),
            "templates": templates,
        },
        "components.json": {
            "schemaVersion": SCHEMA_VERSION,
            "generatedBy": GENERATOR_NAME,
            "componentCount": len(components),
            "components": components,
        },
        "tag-index.json": {
            "schemaVersion": SCHEMA_VERSION,
            "generatedBy": GENERATOR_NAME,
            "tags": tag_index(search),
        },
    }


def write_indexes(output_dir, root=None, manifest_path=None):
    output_dir = Path(output_dir)
    written = []
    for filename, payload in build_indexes(root=root, manifest_path=manifest_path).items():
        written.append(write_json(output_dir / filename, payload))
    return written


def check_indexes(output_dir, root=None, manifest_path=None):
    failures = []
    output_dir = Path(output_dir)
    for filename, payload in build_indexes(root=root, manifest_path=manifest_path).items():
        path = output_dir / filename
        expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if not path.exists():
            failures.append((path, "missing"))
        elif path.read_text(encoding="utf-8") != expected:
            failures.append((path, "changed"))
    return failures


def run_self_tests():
    indexes = build_indexes()
    assert indexes["search-index.json"]["entryCount"] > 0
    assert indexes["templates.json"]["templateCount"] > 0
    assert indexes["components.json"]["componentCount"] > 0
    assert indexes["tag-index.json"]["tags"]
    print("search_index.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate static search indexes for assets, templates, themes, components, and tags.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--manifest", default="assets/manifest.json", help="Manifest path relative to repo root.")
    parser.add_argument("--output-dir", default="site/data", help="Output directory for index JSON files.")
    parser.add_argument("--check", action="store_true", help="Verify indexes are current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run indexer self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output_dir = root / args.output_dir
    manifest = root / args.manifest
    if args.check:
        failures = check_indexes(output_dir, root, manifest)
        if failures:
            for path, status in failures:
                print(f"::error file={rel_path(path, root)}::Search index is {status}. Run npm run generate:indexes.")
            return 1
        print("Search indexes are current.")
        return 0

    written = write_indexes(output_dir, root, manifest)
    for path in written:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
