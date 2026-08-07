from pathlib import Path
import argparse
from collections import Counter
import html
import json
import re
import sys
import tempfile


DEFAULT_REPO_RAW_BASE = "https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master"
DEFAULT_PROFILE_URL = "https://github.com/HiradEmami"

CATEGORY_DESCRIPTIONS = {
    "banners": "Wide visual strips for README hero areas, section breaks, and decorative project branding.",
    "buttons": "Clickable-looking SVG button assets for README calls to action, profile links, social links, and status actions.",
    "dividers": "Horizontal separators that split README sections with static or animated visual treatments.",
    "file_headers": "Header graphics for common repository files such as security, contributing, and code of conduct documents.",
    "headers": "Title and section header graphics for stronger README hierarchy.",
    "icons": "Small SVG symbols for UI, status, development, data, effects, and navigation use cases.",
    "loadings": "Animated loading indicators and motion accents for status-heavy README sections.",
    "personal": "Personal portfolio and project-story visuals for profile READMEs and author pages.",
    "progress_bars": "Progress indicators for roadmaps, milestones, lifecycle states, and completion summaries.",
    "visuals": "Larger conceptual illustrations for AI, systems, infrastructure, collaboration, and product storytelling.",
}

BEST_FOR = {
    "banners": "README hero strips, project identity blocks, release announcements, and high-impact section openings.",
    "buttons": "README calls to action, install links, documentation links, sponsorship links, profile links, and status actions.",
    "dividers": "Breaking long README pages into readable sections without adding heavy layout components.",
    "file_headers": "Giving policy, contribution, security, support, changelog, and documentation files a polished first impression.",
    "headers": "Replacing plain section titles with richer visual anchors in showcase READMEs and profile pages.",
    "icons": "Inline metadata, feature lists, status rows, navigation cues, and compact UI-style README sections.",
    "loadings": "Build, deployment, async workflow, roadmap, and live-status sections where motion communicates activity.",
    "personal": "Profile READMEs, portfolio intros, maintainer pages, and personal project storytelling.",
    "progress_bars": "Roadmaps, maturity markers, skill indicators, rollout status, and project completion summaries.",
    "visuals": "Large conceptual sections for architecture, AI systems, observability, security, and product narratives.",
}

SUBCATEGORY_DESCRIPTIONS = {
    "animated": "Animated variants for motion-first README accents.",
    "static": "Static variants for cleaner, low-motion README layouts.",
    "energy": "High-energy banner assets with beams, cores, pulses, and sci-fi motion.",
    "minimal": "Restrained banner assets built around simple geometry, dots, lines, and subtle motion.",
    "particles": "Particle-based banners for network, sparkle, orbit, and ambient visual effects.",
    "waves": "Wave-style banners for smooth section transitions and soft hero treatments.",
    "core": "General-purpose interface and project icons.",
    "cta": "Primary call-to-action buttons for install, docs, launch, demo, API, and template links.",
    "data-ai": "Data, AI, robotics, neural, server, and signal-themed icons.",
    "decorative": "Decorative accents for visual rhythm and lightweight ornamentation.",
    "dev": "Developer workflow icons for code, CLI, builds, commits, downloads, and pipelines.",
    "devops": "Infrastructure and operations icons for signals, scanning, heartbeat, and reactor-style states.",
    "effects": "Motion and special-effect icons such as orbits, portals, glitches, ripples, and spinners.",
    "navigation": "Navigation-oriented symbols and movement cues.",
    "objects": "Object-based icons such as clocks, calendars, rockets, locations, and other concrete symbols.",
    "status": "Status and alert icons for success, warning, danger, info, live, and deprecated states.",
    "social": "Profile, community, sponsor, portfolio, and discussion buttons.",
    "ui": "Common UI icons such as arrows, chevrons, filters, search, and menu controls.",
}

TAG_KEYWORDS = {
    "accessibility": {"a11y", "accessibility", "audit"},
    "ai": {"ai", "agent", "embedding", "inference", "model", "neural", "prompt", "rag", "token", "vector"},
    "api": {"api", "endpoint", "reference", "rest"},
    "architecture": {"architecture", "circuit", "graph", "lineage", "network", "pipeline", "schema", "system"},
    "badge": {"badge", "tag"},
    "button": {"button", "cta", "launch", "open", "view"},
    "build": {"build", "ci", "cd", "deploy", "deployment", "release", "shipping"},
    "code": {"bracket", "cli", "code", "command", "debug", "dev", "lint", "module", "script", "terminal"},
    "data": {"cache", "data", "database", "dataset", "db", "feature", "matrix", "packet"},
    "docs": {"changelog", "contributing", "docs", "examples", "faq", "guide", "readme", "usage"},
    "energy": {"arc", "core", "energy", "flux", "glow", "laser", "neon", "plasma", "pulse", "reactor"},
    "governance": {"code_of_conduct", "funding", "governance", "license", "sponsors"},
    "infrastructure": {"cluster", "docker", "edge", "env", "observability", "pod", "runtime", "server", "stack"},
    "minimal": {"clean", "minimal", "simple", "soft"},
    "motion": {"animated", "bouncing", "loading", "orbit", "rotating", "scan", "spinner", "sweep", "wave"},
    "navigation": {"anchor", "breadcrumb", "compass", "jump", "navigation", "route", "sidebar", "waypoint"},
    "profile": {"personal", "portfolio", "profile"},
    "security": {"key", "policy", "privacy", "radar", "secret", "secure", "security", "shield", "vault"},
    "status": {"blocked", "deprecated", "experimental", "health", "live", "paused", "queued", "status", "verified"},
    "testing": {"benchmark", "eval", "experiment", "harness", "matrix", "test", "testing"},
}

CATEGORY_TAGS = {
    "banners": {"hero", "wide"},
    "buttons": {"button", "cta"},
    "dividers": {"separator"},
    "file_headers": {"docs", "header"},
    "headers": {"header", "title"},
    "icons": {"icon"},
    "loadings": {"loading", "motion"},
    "personal": {"personal", "profile"},
    "progress_bars": {"progress", "status"},
    "visuals": {"illustration", "visual"},
}

SUBCATEGORY_TAGS = {
    "animated": {"animated", "motion"},
    "static": {"static"},
    "loadings": {"loading", "motion"},
    "energy": {"energy"},
    "minimal": {"minimal"},
    "particles": {"particles"},
    "waves": {"wave"},
    "core": {"core"},
    "cta": {"button", "cta"},
    "data-ai": {"ai", "data"},
    "decorative": {"decorative"},
    "dev": {"code", "developer"},
    "devops": {"devops", "infrastructure"},
    "effects": {"effects", "motion"},
    "navigation": {"navigation"},
    "objects": {"object"},
    "status": {"status"},
    "social": {"social", "profile"},
    "ui": {"ui"},
}


def titleize(name):
    words = name.replace("_", " ").replace("-", " ").split()
    acronyms = {
        "ai": "AI",
        "api": "API",
        "cli": "CLI",
        "ci": "CI",
        "ui": "UI",
        "ux": "UX",
        "devops": "DevOps",
    }
    return " ".join(acronyms.get(word.lower(), word.title()) for word in words)


def singularize(name):
    if name == "banners":
        return "banner"
    if name == "headers":
        return "header"
    if name == "icons":
        return "icon"
    if name == "loadings":
        return "loading"
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def clean_asset_name(path):
    return path.stem


def asset_count(units):
    return sum(len(assets) for _, assets in units)


def animation_label(asset_path):
    path_text = asset_path.as_posix().lower()
    if "/animated/" in path_text or "animated" in path_text:
        return "Animated"
    try:
        source = asset_path.read_text(encoding="utf-8").lower()
    except UnicodeDecodeError:
        return "Static or subtle motion"
    if "<animate" in source or "@keyframes" in source:
        return "Animated"
    return "Static or subtle motion"


def asset_tags(category, unit_name, asset_path):
    tags = set()
    tags.update(CATEGORY_TAGS.get(category, set()))
    tags.update(SUBCATEGORY_TAGS.get(unit_name, set()))

    if animation_label(asset_path) == "Animated":
        tags.update({"animated", "motion"})
    else:
        tags.add("static")

    searchable = " ".join(
        [
            category,
            unit_name,
            asset_path.stem,
            asset_path.parent.name,
        ]
    ).lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", searchable)
    tokens = set(normalized.split())
    compact = normalized.replace(" ", "_")

    for tag, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            keyword_text = keyword.lower()
            if "_" in keyword_text:
                matched = keyword_text in compact
            else:
                matched = keyword_text in tokens
            if matched:
                tags.add(tag)
                break

    return sorted(tags)


def format_tags(tags):
    return ", ".join(f"`{tag}`" for tag in tags)


def top_tags_for_assets(category, unit_name, assets, limit=8):
    counts = Counter()
    for asset_path in assets:
        counts.update(asset_tags(category, unit_name, asset_path))
    return counts.most_common(limit)


def top_tags_for_units(category, units, limit=12):
    counts = Counter()
    for unit_name, assets in units:
        for asset_path in assets:
            counts.update(asset_tags(category, unit_name, asset_path))
    return counts.most_common(limit)


def format_tag_summary(tag_counts):
    if not tag_counts:
        return "_No tags found._"
    return ", ".join(f"`{tag}` ({count})" for tag, count in tag_counts)


def asset_record(repo_root, category, unit_name, asset_path, raw_base):
    return {
        "name": clean_asset_name(asset_path),
        "category": category,
        "subcategory": unit_name,
        "path": relative_asset_path(repo_root, asset_path),
        "rawUrl": raw_url(raw_base, repo_root, asset_path),
        "type": animation_label(asset_path),
        "tags": asset_tags(category, unit_name, asset_path),
    }


def category_units(category_dir):
    subdirs = sorted([item for item in category_dir.iterdir() if item.is_dir()], key=lambda p: p.name.lower())
    if subdirs:
        return [(subdir.name, sorted(subdir.rglob("*.svg"), key=lambda p: p.as_posix().lower())) for subdir in subdirs]
    return [(category_dir.name, sorted(category_dir.glob("*.svg"), key=lambda p: p.name.lower()))]


def relative_asset_path(repo_root, asset_path):
    return asset_path.relative_to(repo_root).as_posix()


def raw_url(raw_base, repo_root, asset_path):
    return f"{raw_base.rstrip('/')}/{relative_asset_path(repo_root, asset_path)}"


def markdown_embed(asset_name, asset_url, profile_url):
    return f"[![{asset_name}]({asset_url})]({profile_url})"


def html_embed(asset_name, asset_url, profile_url):
    escaped_name = html.escape(asset_name, quote=True)
    escaped_url = html.escape(asset_url, quote=True)
    escaped_profile = html.escape(profile_url, quote=True)
    return (
        f'<a href="{escaped_profile}">\n'
        f'  <img src="{escaped_url}" alt="{escaped_name}" />\n'
        f"</a>"
    )


def full_preview_filename(category, unit_name):
    prefix = singularize(category)
    if unit_name == category:
        return f"full_{prefix}_preview.md"
    return f"full_{prefix}_{slugify(unit_name).replace('-', '_')}_preview.md"


def write_index(preview_root, categories):
    lines = [
        "# Asset previews",
        "",
        "Generated preview indexes for the SVG asset library. Do not edit these files by hand; regenerate them with `npm run generate:previews`.",
        "",
        "## Category index",
        "",
        "| Category | Preview | Best for |",
        "| --- | --- | --- |",
    ]

    for category in categories:
        lines.append(
            f"| {titleize(category)} | [`{category}.md`](./{category}.md) | {BEST_FOR.get(category, 'README visual composition and reusable SVG previews.')} |"
        )

    lines.append("")
    output_file = preview_root / "README.md"
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return [output_file]


def write_category_page(repo_root, preview_root, category_dir, raw_base, profile_url):
    category = category_dir.name
    units = category_units(category_dir)
    preview_category_dir = preview_root / category
    preview_category_dir.mkdir(parents=True, exist_ok=True)
    written_files = []

    highlights = []
    for _, assets in units:
        highlights.extend(assets[: max(0, 10 - len(highlights))])
        if len(highlights) >= 10:
            break

    lines = [
        f"# {titleize(category)}",
        "",
        CATEGORY_DESCRIPTIONS.get(category, f"Preview assets from the `{category}/` category."),
        "",
        "Generated from `assets/`. Do not edit this page directly; run `npm run generate:previews` after asset changes.",
        "",
        "## At a glance",
        "",
        f"- Assets: {asset_count(units)}",
        f"- Groups: {len(units)}",
        f"- Best for: {BEST_FOR.get(category, 'README visual composition and reusable SVG previews.')}",
        f"- Category tags: {format_tags(sorted(CATEGORY_TAGS.get(category, {category})))}",
        "",
        "## Tag summary",
        "",
        format_tag_summary(top_tags_for_units(category, units, limit=12)),
        "",
        "## Full previews",
        "",
        "| Group | Count | Description | Full preview |",
        "| --- | ---: | --- | --- |",
    ]

    for unit_name, assets in units:
        preview_file = preview_category_dir / full_preview_filename(category, unit_name)
        label = titleize(unit_name) if unit_name != category else f"All {titleize(category)}"
        description = SUBCATEGORY_DESCRIPTIONS.get(unit_name, CATEGORY_DESCRIPTIONS.get(category, "SVG asset previews."))
        lines.append(f"| {label} | {len(assets)} | {description} | [Open](./{category}/{preview_file.name}) |")

    if highlights:
        lines.extend(["", "## Highlights", ""])
        for asset_path in highlights:
            name = clean_asset_name(asset_path)
            url = raw_url(raw_base, repo_root, asset_path)
            rel_path = relative_asset_path(repo_root, asset_path)
            tags = asset_tags(category, asset_path.parent.name if asset_path.parent != category_dir else category, asset_path)
            lines.extend(
                [
                    f"### {name}",
                    "",
                    markdown_embed(name, url, profile_url),
                    "",
                    f"- Tags: {format_tags(tags)}",
                    f"- [Source file](../../{rel_path})",
                    f"- [Raw SVG]({url})",
                    "",
                ]
            )

    output_file = preview_root / f"{category}.md"
    output_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    written_files.append(output_file)

    for unit_name, assets in units:
        written_files.append(write_full_preview(repo_root, preview_category_dir, category, unit_name, assets, raw_base, profile_url))

    return written_files


def write_full_preview(repo_root, output_dir, category, unit_name, assets, raw_base, profile_url):
    label = titleize(unit_name) if unit_name != category else titleize(category)
    description = SUBCATEGORY_DESCRIPTIONS.get(unit_name, CATEGORY_DESCRIPTIONS.get(category, "SVG asset previews."))
    lines = [
        f"# Full {label} Preview",
        "",
        description,
        "",
        "Generated from `assets/`. Do not edit this page directly; run `npm run generate:previews` after asset changes.",
        "",
        f"[Back to {titleize(category)}](../{category}.md)",
        "",
        "## Metadata",
        "",
        f"- Category: `{category}`",
        f"- Group: `{unit_name}`",
        f"- Asset count: {len(assets)}",
        f"- Best for: {SUBCATEGORY_DESCRIPTIONS.get(unit_name, BEST_FOR.get(category, 'README visual composition and reusable SVG previews.'))}",
        f"- Group tags: {format_tags(sorted(SUBCATEGORY_TAGS.get(unit_name, {unit_name})))}",
        "",
        "## Compact index",
        "",
        f"Top tags: {format_tag_summary(top_tags_for_assets(category, unit_name, assets, limit=10))}",
        "",
        "| Asset | Type | Tags | Preview | Source | Raw |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for asset_path in assets:
        name = clean_asset_name(asset_path)
        url = raw_url(raw_base, repo_root, asset_path)
        rel_path = relative_asset_path(repo_root, asset_path)
        tags = asset_tags(category, unit_name, asset_path)
        lines.append(f"| `{name}` | {animation_label(asset_path)} | {format_tags(tags)} | [Jump](#{slugify(name)}) | [Source](../../../{rel_path}) | [Raw SVG]({url}) |")

    lines.extend(
        [
            "",
            "## Visual previews",
            "",
        ]
    )

    for asset_path in assets:
        name = clean_asset_name(asset_path)
        url = raw_url(raw_base, repo_root, asset_path)
        rel_path = relative_asset_path(repo_root, asset_path)
        tags = asset_tags(category, unit_name, asset_path)

        lines.extend(
            [
                f"## {name}",
                "",
                markdown_embed(name, url, profile_url),
                "",
                "### Copy this asset",
                "",
                "<details>",
                "<summary>Markdown</summary>",
                "",
                "```markdown",
                markdown_embed(name, url, profile_url),
                "```",
                "",
                "</details>",
                "",
                "<details>",
                "<summary>HTML</summary>",
                "",
                "```html",
                html_embed(name, url, profile_url),
                "```",
                "",
                "</details>",
                "",
                "### Details",
                "",
                f"- Type: {animation_label(asset_path)}",
                f"- Tags: {format_tags(tags)}",
                f"- Anchor: `#{slugify(name)}`",
                f"- [Source file](../../../{rel_path})",
                f"- [Raw SVG]({url})",
                "",
            ]
        )

    output_file = output_dir / full_preview_filename(category, unit_name)
    output_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_file


def discover_categories(assets_root):
    return sorted([item for item in assets_root.iterdir() if item.is_dir()], key=lambda p: p.name.lower())


def parse_category_filters(values):
    if not values:
        return None

    categories = []
    for value in values:
        categories.extend([part.strip() for part in value.split(",") if part.strip()])
    return sorted(set(categories), key=str.lower)


def select_categories(categories, selected_names):
    if not selected_names:
        return categories

    by_name = {category.name: category for category in categories}
    unknown = sorted(set(selected_names) - set(by_name))
    if unknown:
        available = ", ".join(sorted(by_name))
        raise ValueError(f"Unknown category filter(s): {', '.join(unknown)}. Available categories: {available}")

    return [by_name[name] for name in selected_names]


def remove_empty_dirs(root):
    for path in sorted([item for item in root.rglob("*") if item.is_dir()], key=lambda p: len(p.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def cleanup_generated_files(preview_root, written_files, selected_categories=None):
    written = {path.resolve() for path in written_files}

    if selected_categories:
        candidates = []
        for category in selected_categories:
            summary = preview_root / f"{category}.md"
            if summary.exists():
                candidates.append(summary)
            category_dir = preview_root / category
            if category_dir.exists():
                candidates.extend([path for path in category_dir.rglob("*") if path.is_file()])
    else:
        candidates = [path for path in preview_root.rglob("*") if path.is_file()]

    removed = []
    for path in candidates:
        if path.resolve() not in written:
            path.unlink()
            removed.append(path)

    remove_empty_dirs(preview_root)
    return removed


def generate_previews(repo_root, assets_dir, output_dir, raw_base, profile_url, category_filters=None, clean=True):
    assets_root = repo_root / assets_dir
    preview_root = repo_root / output_dir

    if not assets_root.exists():
        raise FileNotFoundError(f"Assets directory does not exist: {assets_root}")

    preview_root.mkdir(parents=True, exist_ok=True)
    all_categories = discover_categories(assets_root)
    categories = select_categories(all_categories, category_filters)
    written_files = []

    if not category_filters:
        written_files.extend(write_index(preview_root, [category.name for category in all_categories]))
    for category_dir in categories:
        written_files.extend(write_category_page(repo_root, preview_root, category_dir, raw_base, profile_url))

    removed_files = []
    if clean:
        removed_files = cleanup_generated_files(
            preview_root,
            written_files,
            [category.name for category in categories] if category_filters else None,
        )

    return len(categories), preview_root, removed_files


def write_manifest(repo_root, assets_dir, output_file, raw_base, category_filters=None):
    assets_root = repo_root / assets_dir
    categories = select_categories(discover_categories(assets_root), category_filters)
    records = []

    for category_dir in categories:
        category = category_dir.name
        for unit_name, assets in category_units(category_dir):
            records.extend(asset_record(repo_root, category, unit_name, asset_path, raw_base) for asset_path in assets)

    payload = {
        "assetCount": len(records),
        "categories": [category.name for category in categories],
        "assets": records,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_file, len(records)


def relative_files(root):
    if not root.exists():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def filter_category_files(files, category_filters):
    if not category_filters:
        return files
    return {
        path
        for path in files
        if any(path == f"{category}.md" or path.startswith(f"{category}/") for category in category_filters)
    }


def compare_preview_dirs(expected_root, actual_root, category_filters=None):
    expected_files = relative_files(expected_root)
    actual_files = relative_files(actual_root)
    expected_files = filter_category_files(expected_files, category_filters)
    actual_files = filter_category_files(actual_files, category_filters)

    missing = sorted(expected_files - actual_files)
    extra = sorted(actual_files - expected_files)
    changed = []

    for relative_path in sorted(expected_files & actual_files):
        expected = expected_root / relative_path
        actual = actual_root / relative_path
        if expected.read_bytes() != actual.read_bytes():
            changed.append(relative_path)

    return missing, changed, extra


def check_previews(repo_root, assets_dir, output_dir, raw_base, profile_url, category_filters=None):
    actual_root = repo_root / output_dir

    with tempfile.TemporaryDirectory(prefix=".asset-preview-check-", dir=repo_root) as temp_dir:
        temp_output = Path(temp_dir) / "previews" / "assets"
        generate_previews(
            repo_root,
            assets_dir,
            temp_output.relative_to(repo_root),
            raw_base,
            profile_url,
            category_filters=category_filters,
        )
        return compare_preview_dirs(temp_output, actual_root, category_filters=category_filters)


def print_check_failures(missing, changed, extra):
    print("Asset previews are stale. Regenerate them with:")
    print()
    print("  python src/modules/generators/generate_asset_previews.py")
    print()

    groups = [
        ("Missing files", missing),
        ("Changed files", changed),
        ("Extra files", extra),
    ]

    for label, files in groups:
        if not files:
            continue
        print(f"{label}:")
        for path in files[:20]:
            print(f"  - {path}")
            print(f"::error file={path}::{label[:-1] if label.endswith('s') else label}: {path}")
        if len(files) > 20:
            print(f"  ... and {len(files) - 20} more")
        print()


def run_self_tests():
    assert titleize("data-ai") == "Data AI"
    assert titleize("devops") == "DevOps"
    assert full_preview_filename("banners", "energy") == "full_banner_energy_preview.md"
    assert full_preview_filename("progress_bars", "progress_bars") == "full_progress_bar_preview.md"
    assert parse_category_filters(["icons,loadings", "visuals"]) == ["icons", "loadings", "visuals"]
    assert filter_category_files({"README.md", "icons.md", "icons/full.md", "loadings.md"}, ["icons"]) == {
        "icons.md",
        "icons/full.md",
    }
    print("generate_asset_previews.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown preview pages for SVG assets.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--assets-dir", default="assets", help="Asset directory relative to the repo root.")
    parser.add_argument("--output-dir", default="previews/assets", help="Output directory relative to the repo root.")
    parser.add_argument("--raw-base", default=DEFAULT_REPO_RAW_BASE, help="Raw GitHub base URL.")
    parser.add_argument("--profile-url", default=DEFAULT_PROFILE_URL, help="Link target for preview image embeds.")
    parser.add_argument(
        "--category",
        action="append",
        help="Generate or check one category. Can be passed multiple times or as a comma-separated list.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove obsolete generated preview files after writing current output.",
    )
    parser.add_argument("--manifest", help="Optional JSON asset metadata output path.")
    parser.add_argument("--self-test", action="store_true", help="Run focused generator helper tests and exit.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated previews are current without modifying the output directory.",
    )
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return

    repo_root = Path(args.repo_root).resolve()
    category_filters = parse_category_filters(args.category)

    if args.check:
        try:
            missing, changed, extra = check_previews(
                repo_root,
                Path(args.assets_dir),
                Path(args.output_dir),
                args.raw_base,
                args.profile_url,
                category_filters=category_filters,
            )
        except ValueError as error:
            print(error, file=sys.stderr)
            sys.exit(2)
        if missing or changed or extra:
            print_check_failures(missing, changed, extra)
            sys.exit(1)

        print("Asset previews are current.")
        return

    try:
        category_count, preview_root, removed_files = generate_previews(
            repo_root,
            Path(args.assets_dir),
            Path(args.output_dir),
            args.raw_base,
            args.profile_url,
            category_filters=category_filters,
            clean=not args.no_clean,
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        sys.exit(2)

    scope = f"selected category count {category_count}" if category_filters else f"{category_count} asset categories"
    print(f"Generated previews for {scope} in {preview_root}")
    if removed_files:
        print(f"Removed {len(removed_files)} obsolete generated preview file(s).")

    if args.manifest:
        manifest_path, asset_total = write_manifest(
            repo_root,
            Path(args.assets_dir),
            repo_root / args.manifest,
            args.raw_base,
            category_filters=category_filters,
        )
        print(f"Wrote manifest for {asset_total} asset(s) to {manifest_path}")


if __name__ == "__main__":
    main()
