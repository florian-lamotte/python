from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal[
    "DEBUG", 
    "INFO", 
    "WARNING", 
    "ERROR", 
    "CRITICAL"
]

class Settings(BaseSettings):
    # Application
    app_name: str = "API"
    app_description: str = "Prototype d'API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Logging
    log_level: LogLevel = "INFO"
    
    # Database
    database_url: str | None = None # à rendre obligatoire seulement si la base est indispensable

    # attribut spécial de configuration de la classe Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False, # les noms de variables sont insensibles à la casse
        extra="ignore", # ignore les variables inconnues de .env
    )

# décorateur qui met en cache l'objet Settings pour éviter de le recréer à chaque appel de get_settings()
@lru_cache
def get_settings() -> Settings:
    return Settings()