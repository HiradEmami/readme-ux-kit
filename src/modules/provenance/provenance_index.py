from pathlib import Path
import argparse
import json
import re
import tempfile

from src.modules.common.repo import load_json, read_text, rel_path, repo_root, write_json


SCHEMA_VERSION = 1
GENERATOR_NAME = "src/modules/provenance/provenance_index.py"
THIRD_PARTY_DOC = "docs/THIRD_PARTY.md"
UPSTREAM_URL = "https://github.com/OstinUA/Promt-AI-Helper"
UPSTREAM_LICENSE = "The Unlicense"
ASSET_LINK_RE = re.compile(r"\[`([^`]+)`\]\((?:\.\./)?(assets/[^)]+)\)")


def derived_asset_entries(root):
    doc = root / THIRD_PARTY_DOC
    if not doc.exists():
        return []
    entries = []
    for line in read_text(doc).splitlines():
        if not line.strip().startswith("|") or "---" in line:
            continue
        match = ASSET_LINK_RE.search(line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        entries.append(
            {
                "name": cells[0],
                "path": match.group(2),
                "origin": "third-party-derived",
                "source": UPSTREAM_URL,
                "license": UPSTREAM_LICENSE,
                "status": cells[2],
                "notes": cells[3],
                "exists": (root / match.group(2)).exists(),
            }
        )
    return sorted(entries, key=lambda item: item["path"])


def manifest_assets(root, manifest_path):
    if not manifest_path.exists():
        return []
    return load_json(manifest_path).get("assets", [])


def build_provenance(root=None, manifest_path=None):
    root = Path(root or repo_root()).resolve()
    manifest_path = Path(manifest_path or root / "assets" / "manifest.json")
    derived = derived_asset_entries(root)
    derived_by_path = {entry["path"]: entry for entry in derived}
    assets = []
    for asset in manifest_assets(root, manifest_path):
        local_path = asset.get("localPath") or asset.get("path")
        derived_entry = derived_by_path.get(local_path)
        if derived_entry:
            assets.append({**derived_entry, "category": asset.get("category"), "subcategory": asset.get("subcategory")})
        else:
            assets.append(
                {
                    "name": asset.get("name"),
                    "path": local_path,
                    "category": asset.get("category"),
                    "subcategory": asset.get("subcategory"),
                    "origin": "first-party",
                    "source": "readme-ux-kit",
                    "license": "MIT",
                    "status": "Maintained first-party asset",
                    "notes": "Covered by the repository license unless a future provenance entry says otherwise.",
                    "exists": bool(local_path and (root / local_path).exists()),
                }
            )
    origin_counts = {}
    for asset in assets:
        origin_counts[asset["origin"]] = origin_counts.get(asset["origin"], 0) + 1
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATOR_NAME,
        "sourceDocuments": [THIRD_PARTY_DOC],
        "policy": {
            "defaultFirstPartyLicense": "MIT",
            "requiredExternalAssetDocument": THIRD_PARTY_DOC,
            "knownPublicDomainSource": UPSTREAM_URL,
        },
        "summary": {
            "assetCount": len(assets),
            "derivedAssetCount": len(derived),
            "originCounts": dict(sorted(origin_counts.items())),
        },
        "assets": sorted(assets, key=lambda item: item["path"] or ""),
    }


def validation_errors(root=None, manifest_path=None):
    root = Path(root or repo_root()).resolve()
    manifest_path = Path(manifest_path or root / "assets" / "manifest.json")
    errors = []
    doc = root / THIRD_PARTY_DOC
    if not doc.exists():
        return [f"{THIRD_PARTY_DOC} is missing."]
    text = read_text(doc)
    for required in [UPSTREAM_URL, UPSTREAM_LICENSE, "Known Derived Assets"]:
        if required not in text:
            errors.append(f"{THIRD_PARTY_DOC} should mention {required}.")
    manifest_paths = {asset.get("localPath") or asset.get("path") for asset in manifest_assets(root, manifest_path)}
    for entry in derived_asset_entries(root):
        if not entry["exists"]:
            errors.append(f"Derived asset does not exist: {entry['path']}")
        if manifest_paths and entry["path"] not in manifest_paths:
            errors.append(f"Derived asset is not present in manifest: {entry['path']}")
    return errors


def write_provenance(output, root=None, manifest_path=None):
    payload = build_provenance(root, manifest_path)
    return write_json(output, payload), payload["summary"]["assetCount"]


def check_provenance(output, root=None, manifest_path=None):
    payload = build_provenance(root, manifest_path)
    expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = Path(output)
    status = None
    if not output.exists():
        status = "missing"
    elif output.read_text(encoding="utf-8") != expected:
        status = "changed"
    return status, validation_errors(root, manifest_path)


def run_self_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "docs").mkdir()
        (root / "assets" / "file_headers").mkdir(parents=True)
        asset = root / "assets" / "file_headers" / "demo.svg"
        asset.write_text("<svg/>", encoding="utf-8")
        (root / "docs" / "THIRD_PARTY.md").write_text(
            "# Third-Party Asset Provenance\n\n"
            f"{UPSTREAM_URL}\n\n{UPSTREAM_LICENSE}\n\n## Known Derived Assets\n\n"
            "| Asset | Local path | Status | Notes |\n| --- | --- | --- | --- |\n"
            "| Demo | [`assets/file_headers/demo.svg`](../assets/file_headers/demo.svg) | Modified derivative | Test. |\n",
            encoding="utf-8",
        )
        (root / "assets" / "manifest.json").write_text(
            json.dumps({"assets": [{"name": "Demo", "localPath": "assets/file_headers/demo.svg", "category": "file_headers", "subcategory": "file_headers"}]}),
            encoding="utf-8",
        )
        payload = build_provenance(root)
        assert payload["summary"]["derivedAssetCount"] == 1
        assert validation_errors(root) == []
    print("provenance_index.py self-tests passed.")


def main():
    parser = argparse.ArgumentParser(description="Generate and validate asset provenance metadata.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--manifest", default="assets/manifest.json", help="Manifest path relative to repo root.")
    parser.add_argument("--output", default="assets/provenance.json", help="Provenance JSON path relative to repo root.")
    parser.add_argument("--check", action="store_true", help="Verify provenance data is current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run focused provenance self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    output = root / args.output
    manifest = root / args.manifest
    if args.check:
        status, errors = check_provenance(output, root, manifest)
        if status:
            print(f"::error file={rel_path(output, root)}::Provenance index is {status}. Run npm run generate:provenance.")
        for error in errors:
            print(f"::error::{error}")
        if status or errors:
            return 1
        print("Provenance index is current.")
        return 0

    path, count = write_provenance(output, root, manifest)
    print(f"Wrote provenance for {count} asset(s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
