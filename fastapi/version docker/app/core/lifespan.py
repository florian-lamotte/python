from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.logging_config import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Application starting")

    # Initialisation des ressources
    # Exemple : connexion database

    yield

    # Fermeture des ressources
    # Exemple : fermeture database

    logger.info("Application shutting down")