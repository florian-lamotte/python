import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import get_settings
from app.core.request_context import request_id_ctx

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True

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
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.addFilter(RequestIdFilter())

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s "
        "- request_id=%(request_id)s "
        "- %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.addHandler(file_handler)
    _configured = True

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)