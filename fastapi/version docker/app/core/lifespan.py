from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from fastapi import FastAPI

from app.core.logging_config import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """ Gère le démarrage et l'arrêt des applications """
    
    # Avant yield : démarrage de l'application
    logger.info("Application starting")

    try:
        # Initialisation des ressources
        # Exemple : connexion database

        yield
    finally:
        # Fermeture des ressources
        # Exemple : fermeture database

        # Après yield : arrêt de l'application
        logger.info("Application shutting down")