from __future__ import annotations

from pathlib import Path
import argparse
import json
import shutil
import tempfile

from src.modules.common.repo import repo_root


def manifest_asset_paths(manifest_path: Path) -> list[str]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = payload.get("assets", [])
    paths = [str(item.get("path", "")).replace("\\", "/") for item in assets]
    if not paths or any(not path.startswith("assets/") or not path.endswith(".svg") for path in paths):
        raise ValueError("Asset manifest contains an invalid or empty asset path.")
    if len(paths) != len(set(paths)):
        raise ValueError("Asset manifest contains duplicate asset paths.")
    return paths


def validate_staged_pages(output_dir: Path, manifest_path: Path) -> int:
    required = ("index.html", "styles.css", "app.js", "data/assets.json", ".nojekyll")
    missing_shell = [name for name in required if not (output_dir / name).is_file()]
    if missing_shell:
        raise ValueError("Staged Pages shell is incomplete: " + ", ".join(missing_shell))

    paths = manifest_asset_paths(manifest_path)
    missing_assets = [path for path in paths if not (output_dir / path).is_file()]
    if missing_assets:
        sample = ", ".join(missing_assets[:5])
        raise ValueError(f"Staged Pages artifact is missing {len(missing_assets)} manifest asset(s): {sample}")

    staged_paths = {
        path.relative_to(output_dir).as_posix()
        for path in (output_dir / "assets").rglob("*.svg")
    }
    manifest_paths = set(paths)
    extras = sorted(staged_paths - manifest_paths)
    if extras:
        raise ValueError(f"Staged Pages artifact has {len(extras)} SVG(s) absent from the manifest.")

    return len(paths)


def stage_pages(root: Path, output_dir: Path, safe_parent: Path | None = None) -> int:
    root = root.resolve()
    output_dir = output_dir.resolve()
    safe_parent = Path(safe_parent or root).resolve()
    site_dir = root / "site"
    assets_dir = root / "assets"
    manifest_path = assets_dir / "manifest.json"

    if not site_dir.is_dir() or not assets_dir.is_dir() or not manifest_path.is_file():
        raise ValueError("site/, assets/, and assets/manifest.json are required.")
    if output_dir == safe_parent or safe_parent not in output_dir.parents:
        raise ValueError("Pages output must be a dedicated directory inside its approved staging parent.")

    if output_dir.exists():
        shutil.rmtree(output_dir)

    def ignore_site_assets(directory: str, names: list[str]) -> set[str]:
        return {"assets"} if Path(directory).resolve() == site_dir.resolve() and "assets" in names else set()

    shutil.copytree(site_dir, output_dir, ignore=ignore_site_assets)
    shutil.copytree(assets_dir, output_dir / "assets")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    return validate_staged_pages(output_dir, manifest_path)


def run_self_tests() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "site" / "data").mkdir(parents=True)
        (root / "assets" / "demo").mkdir(parents=True)
        for filename in ("index.html", "styles.css", "app.js"):
            (root / "site" / filename).write_text(filename, encoding="utf-8")
        asset_path = "assets/demo/sample.svg"
        (root / asset_path).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"/>', encoding="utf-8")
        manifest = {"assets": [{"path": asset_path}]}
        manifest_text = json.dumps(manifest)
        (root / "assets" / "manifest.json").write_text(manifest_text, encoding="utf-8")
        (root / "site" / "data" / "assets.json").write_text(manifest_text, encoding="utf-8")
        output = root / "build" / "pages"
        assert stage_pages(root, output) == 1
        assert (output / asset_path).is_file()
        assert validate_staged_pages(output, root / "assets" / "manifest.json") == 1
    print("stage_pages.py self-tests passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a self-contained static Pages artifact with local SVG assets.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--output", default="build/pages", help="Output directory inside the repository.")
    parser.add_argument("--check", action="store_true", help="Build and validate in a temporary directory.")
    parser.add_argument("--self-test", action="store_true", help="Run focused staging self-tests.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    root = Path(args.repo_root).resolve()
    if args.check:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            count = stage_pages(root, temp_root / "pages", safe_parent=temp_root)
        print(f"Pages artifact check passed with {count} local SVG assets.")
        return 0

    output = (root / args.output).resolve()
    count = stage_pages(root, output)
    print(f"Staged {count} local SVG assets in {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
