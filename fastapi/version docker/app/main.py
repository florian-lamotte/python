import time
import uuid

from fastapi import FastAPI, Request

from app.routers import items
from app.logging_config import get_logger, setup_logging
from app.core.config import get_settings
from app.core.request_context import request_id_ctx

settings = get_settings()

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    token = request_id_ctx.set(request_id)
    
    start_time = time.perf_counter()

    method = request.method
    path = request.url.path
    
    try:
        response = await call_next(request)
        
        duration = time.perf_counter() - start_time
        status_code = response.status_code

        message = (
            "%s %s - status=%s - duration=%.3fs"
        )

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

        response.headers["X-Request-ID"] = request_id
        return response
    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "%s %s - exception - duration=%.3fs",
            method,
            path,
            duration,
        )
        raise
    finally:
        request_id_ctx.reset(token)

@app.get("/", tags=["Divers"])
async def read_root():
    return {"message": "Bonjour"}

@app.get("/health", tags=["Monitoring"])
async def health():
    return {"status": "ok"}

app.include_router(items.router)