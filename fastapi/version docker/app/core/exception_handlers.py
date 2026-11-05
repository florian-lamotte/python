from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException

async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    request_id = getattr(
        request.state,
        "request_id",
        None,
    )
    
    headers = {}

    if request_id:
        headers["X-Request-ID"] = request_id

    # request_id est renvoyé dans le corps JSON et les headers HTTP
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "request_id": request_id,
        },
        headers=headers,
    )