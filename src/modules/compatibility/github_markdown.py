from pathlib import Path
import argparse
import json
import re

from src.modules.common.repo import iter_markdown_files, load_json, markdown_links, rel_path, repo_root, strip_fenced_blocks, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/compatibility/github_markdown.py"
HTML_TAG_RE = re.compile(r"</?([a-zA-Z][a-zA-Z0-9-]*)\b")
ALLOWED_HTML_TAGS = {
    "a",
    "br",
    "code",
    "dd",
    "del",
    "details",
    "div",
    "dl",
    "dt",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "img",
    "kbd",
    "li",
    "ol",
    "p",
    "picture",
    "pre",
    "source",
    "span",
    "strong",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
}
RAW_BASE = "https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/"


def finding(code, path, message, severity="warning"):
    return {"code": code, "path": path, "message": message, "severity": severity}


def markdown_html_findings(root):
    findings = []
    for path in iter_markdown_files(root, ["README.md", "docs", "components", "templates", "themes"]):
        text = strip_fenced_blocks(path.read_text(encoding="utf-8"))
        for tag in sorted({match.group(1).lower() for match in HTML_TAG_RE.finditer(text)}):
            if tag not in ALLOWED_HTML_TAGS:
                findings.append(finding("github-html-unknown-tag", rel_path(path, root), f"Review GitHub support for <{tag}>."))
        if len(text.splitlines()) > 700:
            findings.append(finding("long-markdown-document", rel_path(path, root), "Document is long enough to need extra navigation."))
    return findings


def raw_url_findings(root):
    findings = []
    for path in iter_markdown_files(root, ["README.md", "docs", "components", "templates", "themes"]):
        for link in markdown_links(path):
            if "raw.githubusercontent.com" not in link:
                continue
            if not link.startswith(RAW_BASE):
                findings.append(
                    finding(
                        "raw-url-external-owner",
                        rel_path(path, root),
                        f"Raw GitHub URL is outside the expected public asset base: {link}",
                        severity="info",
                    )
                )
    return findings


def svg_findings(root):
    findings = []
    analysis_path = root / "site" / "data" / "svg-analysis.json"
    if not analysis_path.exists():
        return [finding("missing-svg-analysis", "site/data/svg-analysis.json", "Run SVG analysis before compatibility checks.", severity="error")]
    analysis = load_json(analysis_path)
    for asset in analysis.get("assets", []):
        flags = set(asset.get("flags", []))
        if "large-file" in flags:
            findings.append(finding("large-svg-readme-cost", asset["path"], "Large SVG may slow README rendering.", severity="info"))
        if "high-motion" in flags:
            findings.append(finding("high-motion-readme-cost", asset["path"], "High-motion SVG should be used sparingly in README pages.", severity="info"))
        if "contrast-risk" in flags:
            findings.append(finding("svg-contrast-risk", asset["path"], "SVG has possible text/background contrast risk."))
        if "accessibility-risk" in flags:
            findings.append(finding("svg-accessibility-risk", asset["path"], "SVG may need title, desc, role, or aria-label review."))
    return findings


def build_compatibility_report(root=None):
    root = Path(root or repo_root()).resolve()
    findings = markdown_html_findings(root) + raw_url_findings(root) + svg_findings(root)
    counts = {}
    severity_counts = {}
    for item in findings:
        counts[item["code"]] = counts.get(item["code"], 0) + 1
        severity_counts[item["severity"]] = severity_counts.get(item["severity"], 0) + 1
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "findingCount": len(findings),
        "summary": {
            "codeCounts": dict(sorted(counts.items())),
            "severityCounts": dict(sorted(severity_counts.items())),
        },
        "findings": sorted(findings, key=lambda item: (item["severity"], item["path"], item["code"], item["message"])),
    }


def write_compatibility_report(output, root=None):
    payload = build_compatibility_report(root)
    return write_json(output, payload), payload["findingCount"]


def check_compatibility_report(output, root=None):
    payload = build_compatibility_report(root)
    expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = Path(output)
    status = None
    if not output.exists():
        status = "missing"
    elif output.read_text(encoding="utf-8") != expected:
        status = "changed"
    errors = [item for item in payload["findings"] if item["severity"] == "error"]
    return status, errors


def run_self_tests():
    assert "details" in ALLOWED_HTML_TAGS
    assert "script" not in ALLOWED_HTML_TAGS
    payload = build_compatibility_report()
    assert "summary" in payload
    print("github_markdown.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate and check GitHub README compatibility signals.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="site/data/compatibility-report.json", help="Compatibility report path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify compatibility report is current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused compatibility self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    if args.check:
        status, errors = check_compatibility_report(output, root)
        if status:
            print(f"::error file={rel_path(output, root)}::Compatibility report is {status}. Run npm run generate:compatibility.")
        for item in errors:
            print(f"::error file={item['path']}::{item['code']}: {item['message']}")
        if status or errors:
            return 1
        print("Compatibility report is current.")
        return 0

    path, count = write_compatibility_report(output, root)
    print(f"Wrote {count} compatibility finding(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
