from pathlib import Path
import json
import re


HTTP_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
FENCED_BLOCK_RE = re.compile(r"```.*?```|````.*?````", re.DOTALL)
INLINE_MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_REF_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
EXPLICIT_ANCHOR_RE = re.compile(r"""<a\s+[^>]*id=["']([^"']+)["']""", re.IGNORECASE)


def repo_root():
    return Path(__file__).resolve().parents[3]


def rel_path(path, root=None):
    root = root or repo_root()
    return Path(path).resolve().relative_to(root.resolve()).as_posix()


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def strip_fenced_blocks(text):
    output = []
    active = None
    for line in text.splitlines():
        stripped = line.lstrip()
        match = re.match(r"(`{3,}|~{3,})", stripped)
        if match:
            marker = match.group(1)
            fence = (marker[0], len(marker))
            if active is None:
                active = fence
            elif fence[0] == active[0] and fence[1] >= active[1]:
                active = None
            output.append("")
            continue
        output.append("" if active else line)
    return "\n".join(output)


def is_external_url(value):
    return bool(HTTP_RE.match(value)) or value.startswith("//")


def is_placeholder_url(value):
    lowered = value.lower()
    placeholders = [
        "owner",
        "repo",
        "username",
        "package_name",
        "project_name",
        "service_name",
        "example.com",
        "your-",
        "your_",
        "todo",
    ]
    return any(token in lowered for token in placeholders)


def split_link_target(target):
    target = target.strip()
    if not target or target.startswith("#"):
        return "", target[1:] if target.startswith("#") else ""
    path, _, anchor = target.partition("#")
    return path.split("?", 1)[0], anchor


def markdown_links(path):
    text = strip_fenced_blocks(read_text(path))
    links = []
    for match in INLINE_MARKDOWN_LINK_RE.finditer(text):
        links.append(match.group(1))
    for match in HTML_REF_RE.finditer(text):
        links.append(match.group(1))
    return links


def slugify_heading(value):
    value = re.sub(r"<[^>]+>", "", value)
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    return value.strip("-")


def markdown_anchors(path):
    text = strip_fenced_blocks(read_text(path))
    anchors = set()
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            anchors.add(slugify_heading(match.group(2)))
    anchors.update(EXPLICIT_ANCHOR_RE.findall(text))
    return anchors


def iter_markdown_files(root, include_dirs=None):
    root = Path(root)
    if include_dirs:
        files = []
        for directory in include_dirs:
            target = root / directory
            if target.is_file() and target.suffix.lower() == ".md":
                files.append(target)
            elif target.exists():
                files.extend(target.rglob("*.md"))
        return sorted(files, key=lambda path: path.as_posix().lower())
    return sorted(root.rglob("*.md"), key=lambda path: path.as_posix().lower())


def iter_svg_files(root):
    return sorted(Path(root).rglob("*.svg"), key=lambda path: path.as_posix().lower())


def natural_title(path):
    stem = Path(path).stem
    return " ".join(part.upper() if part in {"api", "ci", "ui", "ux", "ml", "ai"} else part.title() for part in re.split(r"[-_]+", stem))
