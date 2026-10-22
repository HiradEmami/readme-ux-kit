from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

try:
    from fastapi import Body, FastAPI, HTTPException, Query, Request
    from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response
    from fastapi.staticfiles import StaticFiles
except ModuleNotFoundError as error:
    Body = FastAPI = HTTPException = Query = Request = None
    FileResponse = JSONResponse = PlainTextResponse = Response = StaticFiles = None
    FASTAPI_IMPORT_ERROR = error
else:
    FASTAPI_IMPORT_ERROR = None

from src.app import services


LOCAL_HOSTS = {"127.0.0.1", "::1", "localhost"}
SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
}


def apply_security_headers(response):
    for header_name, header_value in SECURITY_HEADERS.items():
        response.headers.setdefault(header_name, header_value)
    return response


def require_fastapi():
    if FASTAPI_IMPORT_ERROR is not None:
        raise RuntimeError("FastAPI is not installed. Install the src project dependencies, then run `python -m src.app`.")


def is_allowed_host_header(host_header: str) -> bool:
    if not host_header:
        return True
    raw = host_header.strip().lower()
    if raw.startswith("[::1]"):
        return True
    hostname = raw.split(":", 1)[0]
    return hostname in LOCAL_HOSTS


def is_allowed_origin_header(origin_header: str) -> bool:
    if not origin_header:
        return True
    raw = origin_header.strip().lower()
    for prefix in ("http://127.0.0.1", "http://localhost", "http://[::1]", "https://127.0.0.1", "https://localhost", "https://[::1]"):
        if raw == prefix or raw.startswith(f"{prefix}:"):
            return True
    return False


def create_app():
    require_fastapi()
    app = FastAPI(
        title="readme-ux-kit Local Studio",
        description="Local-only interactive wrapper around src/modules.",
        version="1.0.0",
    )
    root = services.root_path()
    static_dir = Path(__file__).resolve().parent / "static"

    @app.middleware("http")
    async def local_only(request: Request, call_next):
        client_host = request.client.host if request.client else ""
        host_header = request.headers.get("host", "")
        origin_header = request.headers.get("origin", "")
        if (
            client_host not in LOCAL_HOSTS
            or not is_allowed_host_header(host_header)
            or not is_allowed_origin_header(origin_header)
        ):
            return apply_security_headers(
                JSONResponse({"detail": "Local Studio only accepts localhost requests."}, status_code=403)
            )
        response = await call_next(request)
        return apply_security_headers(response)

    @app.get("/api/health")
    def health():
        return {"ok": True, "localOnly": True}

    @app.get("/api/summary")
    def summary():
        return services.repository_summary(root)

    @app.get("/api/commands")
    def commands():
        return {"commands": sorted(services.COMMANDS)}

    @app.get("/api/data/{name}")
    def data_file(name: str):
        try:
            return services.load_data(name, root)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail=f"Missing data file: {error}") from error

    @app.get("/api/reports/quality")
    def quality_report():
        return services.build_quality_report(root)

    @app.get("/api/assets")
    def assets(
        q: str = "",
        category: str = "",
        subcategory: str = "",
        tag: str = "",
        animated: bool | None = Query(default=None),
        editorQuality: str = "",
        limit: int = Query(default=240, ge=1, le=1000),
    ):
        return services.list_assets(
            root=root,
            query=q,
            category=category,
            subcategory=subcategory,
            tag=tag,
            animated=animated,
            editor_quality=editorQuality,
            limit=limit,
        )

    @app.get("/api/assets/detail/{asset_path:path}")
    def asset_detail(asset_path: str):
        try:
            return services.asset_detail(asset_path, root)
        except (FileNotFoundError, ValueError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @app.get("/api/assets/source/{asset_path:path}")
    def asset_source(asset_path: str):
        try:
            return Response(services.asset_detail(asset_path, root)["source"], media_type="image/svg+xml")
        except (FileNotFoundError, ValueError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @app.post("/api/svg/edit")
    def svg_edit(payload: dict = Body(...)):
        try:
            return services.edit_svg(payload, root)
        except (ET.ParseError, FileNotFoundError, ValueError, KeyError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.post("/api/gif/export")
    def gif_export(payload: dict = Body(...)):
        try:
            return services.export_gif(payload, root)
        except RuntimeError as error:
            raise HTTPException(status_code=500, detail=str(error)) from error
        except (ET.ParseError, FileNotFoundError, ValueError, KeyError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.get("/api/gif/file/{gif_path:path}")
    def gif_file(gif_path: str):
        try:
            return FileResponse(services.safe_repo_gif_path(gif_path, root), media_type="image/gif")
        except (FileNotFoundError, ValueError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @app.post("/api/run/{command}")
    def run(command: str):
        try:
            result = services.run_command(command, root)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except subprocess.TimeoutExpired as error:
            raise HTTPException(status_code=504, detail=f"Command timed out: {command}") from error
        return JSONResponse(result, status_code=200 if result["ok"] else 500)

    app.mount("/local-assets", StaticFiles(directory=root / "assets"), name="local-assets")
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="studio-static")
    return app

