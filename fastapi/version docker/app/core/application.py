from fastapi import FastAPI

from app.core.config import get_settings
from app.core.lifespan import lifespan
from app.core.logging_config import setup_logging, get_logger
from app.core.exceptions import AppException
from app.core.exception_handlers import app_exception_handler
from app.core.middleware.request_logging import log_requests
from app.routers import items, health, general

def create_app() -> FastAPI:
    settings = get_settings()

    setup_logging()
    
    logger = get_logger(__name__)
    
    logger.info("Creating application")

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    # middlewares
    app.middleware("http")(log_requests)
    
    # routes
    app.include_router(items.router)
    app.include_router(health.router)
    app.include_router(general.router)

    return app