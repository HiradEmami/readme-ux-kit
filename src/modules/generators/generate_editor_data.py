from pathlib import Path
import argparse

try:
    from .editor_presets import check_editor_data, print_check_failures, run_self_tests, write_editor_data
except ImportError:
    from editor_presets import check_editor_data, print_check_failures, run_self_tests, write_editor_data


def main():
    parser = argparse.ArgumentParser(description="Generate static JSON data for the browser-based SVG editor.")
    parser.add_argument("--output-dir", default="site/data", help="Output directory for editor data JSON files.")
    parser.add_argument("--check", action="store_true", help="Verify generated editor data is current without writing.")
    parser.add_argument("--self-test", action="store_true", help="Run editor data tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    output_dir = Path(args.output_dir)
    if args.check:
        failures = check_editor_data(output_dir)
        if failures:
            print_check_failures(failures)
            return 1
        print("Editor data is current.")
        return 0

    written = write_editor_data(output_dir)
    for path in written:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
