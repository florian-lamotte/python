from fastapi import FastAPI, Request
from app.routers import items
from app.logging_config import get_logger
import time

logger = get_logger(__name__)

app = FastAPI(
    title="API",
    description="Prototype d'API",
    version="0.1.0",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
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
                message,
                method,
                path,
                status_code,
                duration,
            )
        elif status_code >= 400:
            logger.warning(
                message,
                method,
                path,
                status_code,
                duration,
            )
        else:
            logger.info(
                message,
                method,
                path,
                status_code,
                duration,
            )

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

@app.get("/", tags=["Divers"])
def read_root():
    return {"message": "Bonjour"}

app.include_router(items.router)