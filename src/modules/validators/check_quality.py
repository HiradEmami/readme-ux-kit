from pathlib import Path
import argparse

from src.modules.validators.repo_quality import collect_quality_issues, print_issues, run_self_tests


def main():
    parser = argparse.ArgumentParser(description="Run repository quality validators.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--self-test", action="store_true", help="Run validator self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    issues = collect_quality_issues(Path(args.repo_root).resolve())
    print_issues(issues)
    return 1 if any(item["severity"] == "error" for item in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
