from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.core.logging_config import get_logger
from app.core.database.database import Base, engine

# importe les modèles pour les enregistrer dans SQLAlchemy
from app.models.item import Item

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """ Gère le démarrage et l'arrêt des applications """
    
    # Avant yield : démarrage de l'application
    logger.info("Application starting")

    try:
        # Initialisation de la base de données
        logger.info("Initializing database")

        Base.metadata.create_all(bind=engine) # créé les tables du modèle

        logger.info("Database initialized successfully")

        yield
    
    except Exception:
        logger.exception("Application lifecycle error")
        raise
    finally:
        # Fermeture des ressources
        engine.dispose() # ferme les connexions SQLAlchemy

        logger.info("Application shutting down")