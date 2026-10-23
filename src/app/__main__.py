import argparse

from src.app.services import run_self_tests


def main():
    parser = argparse.ArgumentParser(description="Run the readme-ux-kit Local Studio.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host. Keep 127.0.0.1 for local-only use.")
    parser.add_argument("--port", default=8787, type=int, help="Bind port.")
    parser.add_argument("--reload", action="store_true", help="Enable uvicorn reload for app development.")
    parser.add_argument("--self-test", action="store_true", help="Run dependency-light app self-tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return 0

    try:
        import uvicorn
    except ModuleNotFoundError:
        print("FastAPI runtime dependencies are not installed.")
        print("Install them with: cd src && uv sync")
        print("Then run: python -m src.app")
        return 1

    uvicorn.run("src.app.api:create_app", factory=True, host=args.host, port=args.port, reload=args.reload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
