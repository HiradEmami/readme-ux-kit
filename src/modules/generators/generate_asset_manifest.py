from pathlib import Path
import argparse
import sys

try:
    from .asset_manifest import (
        DEFAULT_REPO_RAW_BASE,
        check_manifest,
        parse_category_filters,
        print_manifest_check_failure,
        run_self_tests,
        write_manifest,
    )
except ImportError:
    from asset_manifest import (
        DEFAULT_REPO_RAW_BASE,
        check_manifest,
        parse_category_filters,
        print_manifest_check_failure,
        run_self_tests,
        write_manifest,
    )


def main():
    parser = argparse.ArgumentParser(description="Generate editor-ready JSON metadata for SVG assets.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--assets-dir", default="assets", help="Asset directory relative to the repo root.")
    parser.add_argument("--output", default="assets/manifest.json", help="Manifest output path relative to the repo root.")
    parser.add_argument("--raw-base", default=DEFAULT_REPO_RAW_BASE, help="Raw GitHub base URL.")
    parser.add_argument(
        "--category",
        action="append",
        help="Generate or check one category. Can be passed multiple times or as a comma-separated list.",
    )
    parser.add_argument("--check", action="store_true", help="Verify the manifest is current without writing it.")
    parser.add_argument("--self-test", action="store_true", help="Run focused manifest generator tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    repo_root = Path(args.repo_root).resolve()
    output_file = repo_root / args.output
    category_filters = parse_category_filters(args.category)

    try:
        if args.check:
            status, errors = check_manifest(
                repo_root,
                Path(args.assets_dir),
                output_file,
                raw_base=args.raw_base,
                category_filters=category_filters,
            )
            if status:
                print_manifest_check_failure(output_file, status, errors)
                return 1
            print("Asset manifest is current.")
            return 0

        manifest_path, asset_total = write_manifest(
            repo_root,
            Path(args.assets_dir),
            output_file,
            raw_base=args.raw_base,
            category_filters=category_filters,
        )
    except (FileNotFoundError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2

    print(f"Wrote manifest for {asset_total} asset(s) to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
