from fastapi import FastAPI

from app.core.middleware.request_logging import log_requests

def register_middlewares(app: FastAPI) -> None:
    app.middleware("http")(log_requests)
    # app.add_middleware(SecurityHeadersMiddleware)
    # app.add_middleware(CORSMiddleware)