from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.gzip import GZipMiddleware
from pathlib import Path
import logging
import time
import os

from app.routers import home, diagnostic, risques, equipements, carte

BASE_DIR = Path(__file__).resolve().parent

# ── Logging setup (handles Vercel read-only filesystem) ──
_is_vercel = os.environ.get("VERCEL", "") == "1"

if _is_vercel:
    LOG_DIR = Path("/tmp/logs")
else:
    LOG_DIR = BASE_DIR.parent / "logs"

try:
    LOG_DIR.mkdir(exist_ok=True)
    _log_ok = True
except OSError:
    _log_ok = False

# ── Backend logger ──
backend_logger = logging.getLogger("backend")
backend_logger.setLevel(logging.INFO)
if _log_ok:
    _bh = logging.FileHandler(LOG_DIR / "backend.log", encoding="utf-8")
    _bh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    backend_logger.addHandler(_bh)

# ── Frontend logger (written via /api/log endpoint) ──
frontend_logger = logging.getLogger("frontend")
frontend_logger.setLevel(logging.INFO)
if _log_ok:
    _fh = logging.FileHandler(LOG_DIR / "frontend.log", encoding="utf-8")
    _fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    frontend_logger.addHandler(_fh)

app = FastAPI(
    title="SIG Saint-Louis",
    description="Diagnostic Territorial de l'Agglomération de Saint-Louis du Sénégal",
    version="1.0.0",
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=500)


# ── Request logging middleware ──
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000)
    backend_logger.info(
        "%s %s %s  %dms  client=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration,
        request.client.host if request.client else "-",
    )
    return response


# ── Startup / shutdown events ──
@app.on_event("startup")
async def on_startup():
    backend_logger.info("═" * 60)
    backend_logger.info("SERVER STARTED — SIG Saint-Louis v1.0.0")
    backend_logger.info("Static dir : %s", BASE_DIR / "static")
    data_dir = BASE_DIR / "static" / "data"
    if data_dir.exists():
        geojson_count = len(list(data_dir.rglob("*.geojson")))
        img_count = len(list((BASE_DIR / "static" / "img").rglob("*"))) if (BASE_DIR / "static" / "img").exists() else 0
        backend_logger.info("GeoJSON files: %d  |  Images: %d", geojson_count, img_count)
    backend_logger.info("═" * 60)


@app.on_event("shutdown")
async def on_shutdown():
    backend_logger.info("SERVER STOPPED")


# ── Frontend log endpoint ──
@app.post("/api/log")
async def frontend_log(request: Request):
    body = await request.json()
    level = body.get("level", "info").upper()
    message = body.get("message", "")
    page = body.get("page", "")
    log_fn = getattr(frontend_logger, level.lower(), frontend_logger.info)
    log_fn("[%s] %s", page, message)
    return {"ok": True}

# Static files (CSS, JS, GeoJSON, images)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Register routers
app.include_router(home.router)
app.include_router(diagnostic.router, prefix="/diagnostic", tags=["diagnostic"])
app.include_router(risques.router, prefix="/risques", tags=["risques"])
app.include_router(equipements.router, prefix="/equipements", tags=["equipements"])
app.include_router(carte.router, prefix="/carte", tags=["carte"])
