from fastapi import FastAPI

from app.core import (
    get_settings,
    lifespan,
    setup_logging,
    get_logger
)

from app.core.exceptions import AppException, app_exception_handler

from app.core.middleware import register_middlewares

from app.api import register_routers

def create_app() -> FastAPI:
    # Configuration
    settings = get_settings()

    # Logging
    setup_logging(log_level=settings.log_level)
    logger = get_logger(__name__)

    logger.info("Creating application")

    # Création de l'application
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Exception handlers
    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    # Middlewares
    register_middlewares(app)
    
    # Routes
    register_routers(app)
    
    logger.info("Application created successfully")

    return app