from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException

async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "request_id": getattr(
                request.state,
                "request_id",
                None,
            ),
        },
    )