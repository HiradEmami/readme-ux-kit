from pathlib import Path
import argparse
import json
import re

from src.modules.common.repo import is_external_url, is_placeholder_url, rel_path, repo_root, split_link_target, strip_fenced_blocks, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/recipes/recipe_index.py"
HEADING_RE = re.compile(r"^##\s+(.+)$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
WORD_RE = re.compile(r"[a-z0-9]+")


def slug(value):
    tokens = WORD_RE.findall(value.lower())
    return "-".join(tokens)


def split_sections(text):
    sections = []
    active_fence = None
    current_title = None
    current_lines = []
    for line in text.splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            fence = (marker[0], len(marker))
            if active_fence is None:
                active_fence = fence
            elif fence[0] == active_fence[0] and fence[1] >= active_fence[1]:
                active_fence = None

        heading_match = HEADING_RE.match(line.strip()) if active_fence is None else None
        if heading_match:
            if current_title is not None:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = heading_match.group(1).strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)
    if current_title is not None:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return sections


def first_paragraph(section_text):
    for line in strip_fenced_blocks(section_text).splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("|") and not line.startswith("-"):
            return line
    return ""


def section_links(root, source_path, section_text):
    links = []
    for label, target in LINK_RE.findall(strip_fenced_blocks(section_text)):
        path_text, anchor = split_link_target(target)
        if not path_text or is_external_url(path_text) or is_placeholder_url(path_text):
            continue
        target_path = (source_path.parent / path_text).resolve()
        exists = False
        normalized = path_text
        try:
            normalized = rel_path(target_path, root)
            exists = target_path.exists()
        except ValueError:
            exists = False
        links.append(
            {
                "label": label.strip("`") or normalized,
                "target": target,
                "path": normalized,
                "anchor": anchor,
                "exists": exists,
            }
        )
    return links


def build_recipes(root=None):
    root = Path(root or repo_root()).resolve()
    path = root / "docs" / "RECIPES.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    recipes = []
    for title, body in split_sections(text):
        if title.lower() == "final check":
            continue
        links = section_links(root, path, body)
        recipes.append(
            {
                "id": slug(title),
                "title": title,
                "summary": first_paragraph(body),
                "path": rel_path(path, root) + f"#{slug(title)}",
                "links": links,
                "assetCount": sum(1 for item in links if item["path"].startswith("assets/")),
                "componentCount": sum(1 for item in links if item["path"].startswith("components/")),
                "templateCount": sum(1 for item in links if item["path"].startswith("templates/")),
                "themeCount": sum(1 for item in links if item["path"].startswith("themes/")),
                "tags": sorted(set(WORD_RE.findall((title + " " + first_paragraph(body)).lower()))),
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "recipeCount": len(recipes),
        "recipes": recipes,
    }


def build_bundles(root=None):
    root = Path(root or repo_root()).resolve()
    path = root / "docs" / "BUNDLES.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    bundles = []
    for title, body in split_sections(text):
        if title.lower() == "bundle index":
            continue
        bundle_source = body.split("````markdown", 1)[1].split("````", 1)[0].strip() if "````markdown" in body else ""
        links = section_links(root, path, body)
        bundles.append(
            {
                "id": slug(title),
                "title": title,
                "summary": first_paragraph(body),
                "path": rel_path(path, root) + f"#{slug(title)}",
                "links": links,
                "lineCount": len(bundle_source.splitlines()) if bundle_source else 0,
                "containsTemplatePlaceholders": any(token in bundle_source for token in ["OWNER", "REPO", "PROJECT_NAME", "SERVICE_NAME"]),
                "tags": sorted(set(WORD_RE.findall((title + " " + first_paragraph(body)).lower()))),
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "bundleCount": len(bundles),
        "bundles": bundles,
    }


def validation_errors(payload):
    errors = []
    for collection_name, items in [("recipe", payload["recipes.json"]["recipes"]), ("bundle", payload["bundles.json"]["bundles"])]:
        for item in items:
            for link in item["links"]:
                if not link["exists"]:
                    errors.append(f"{collection_name} {item['id']} references missing path: {link['target']}")
    return errors


def build_payloads(root=None):
    return {
        "recipes.json": build_recipes(root),
        "bundles.json": build_bundles(root),
    }


def write_recipe_indexes(output_dir, root=None):
    output_dir = Path(output_dir)
    written = []
    payloads = build_payloads(root)
    for filename, payload in payloads.items():
        written.append(write_json(output_dir / filename, payload))
    return written


def check_recipe_indexes(output_dir, root=None):
    output_dir = Path(output_dir)
    failures = []
    payloads = build_payloads(root)
    for filename, payload in payloads.items():
        path = output_dir / filename
        expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if not path.exists():
            failures.append((path, "missing"))
        elif path.read_text(encoding="utf-8") != expected:
            failures.append((path, "changed"))
    return failures, validation_errors(payloads)


def run_self_tests():
    payloads = build_payloads()
    assert payloads["recipes.json"]["recipeCount"] > 0
    assert payloads["bundles.json"]["bundleCount"] > 0
    print("recipe_index.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate and validate recipe and copy-all bundle metadata.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output-dir", default="site/data", help="Output directory for recipes.json and bundles.json.")
    parser.add_argument("--check", action="store_true", help="Verify recipe and bundle indexes are current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused recipe self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output_dir = root / args.output_dir
    if args.check:
        failures, errors = check_recipe_indexes(output_dir, root)
        for path, status in failures:
            print(f"::error file={rel_path(path, root)}::Recipe index is {status}. Run npm run generate:recipes.")
        for error in errors:
            print(f"::error::{error}")
        if failures or errors:
            return 1
        print("Recipe and bundle indexes are current.")
        return 0

    written = write_recipe_indexes(output_dir, root)
    for path in written:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
