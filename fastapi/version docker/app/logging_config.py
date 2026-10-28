import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import get_settings

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

_configured = False

def setup_logging() -> None:
    global _configured

    if _configured:
        return
    
    settings = get_settings()
    level = getattr(logging, settings.log_level)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("app")
    logger.setLevel(level)
    logger.propagate = False
    
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    _configured = True

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)