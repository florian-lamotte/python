import time
import uuid

from fastapi import Request

from app.core.logging_config import get_logger
from app.core.request_context import request_id_ctx

logger = get_logger(__name__)

async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    token = request_id_ctx.set(request_id)
    request.state.request_id = request_id
    start_time = time.perf_counter()
    method = request.method
    path = request.url.path
    
    try:
        response = await call_next(request)
        
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