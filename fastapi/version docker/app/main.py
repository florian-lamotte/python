import time

from fastapi import FastAPI, Request

from app.routers import items
from app.logging_config import get_logger
from app.core.config import get_settings

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    method = request.method
    path = request.url.path
    
    try:
        response = await call_next(request)
    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "%s %s - exception - duration=%.3fs",
            method,
            path,
            duration,
        )
        raise

    duration = time.perf_counter() - start_time
    status_code = response.status_code
    message = "%s %s - status=%s - duration=%.3fs"

    if status_code >= 500:
        logger.error(
            message, method, path, status_code, duration
        )
    elif status_code >= 400:
        logger.warning(
            message, method, path, status_code, duration
        )
    else:
        logger.info(
            message, method, path, status_code, duration
        )

    return response

@app.get("/", tags=["Divers"])
async def read_root():
    return {"message": "Bonjour"}

@app.get("/health", tags=["Monitoring"])
async def health():
    return {"status": "ok"}

app.include_router(items.router)