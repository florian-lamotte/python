import sys
import logging

from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from threading import Lock

from pythonjsonlogger.json import JsonFormatter

from app.core.config import LogLevel
from app.core.request_context import request_id_var

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILES = {
    "text": LOG_DIR / "app.log",
    "json": LOG_DIR / "app.json.log",
}

LOG_ROTATION_WHEN = "midnight"
LOG_ROTATION_INTERVAL = 1
LOG_BACKUP_COUNT = 0
LOG_ENCODING = "utf-8"
LOG_UTC = True

_configured = False
_config_lock = Lock()

class RequestIdFilter(logging.Filter):
    """ Ajoute l'id de la requête dans les logs """
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True

def get_text_formatter() -> logging.Formatter:
    """ Retourne le formatter texte """

    return logging.Formatter(
        "%(asctime)s - %(levelname)s "
        "- request_id=%(request_id)s "
        "- %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def get_json_formatter() -> JsonFormatter:
    """ Retourne le formatter JSON """

    return JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s "
        "%(message)s %(request_id)s",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "level",
            "name": "logger",
        },
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

def create_stream_handler(level: int) -> logging.Handler:
    """ Crée un handler stdout """

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(get_text_formatter())
    handler.addFilter(RequestIdFilter())

    return handler

def create_file_handler(
    path: Path,
    level: int,
    formatter: logging.Formatter,
) -> logging.Handler:
    """ Crée un handler fichier avec rotation journalière """

    handler = TimedRotatingFileHandler(
        filename=path,
        when=LOG_ROTATION_WHEN,
        interval=LOG_ROTATION_INTERVAL,
        backupCount=LOG_BACKUP_COUNT,
        encoding=LOG_ENCODING,
        utc=LOG_UTC,
    )

    handler.setLevel(level)
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())

    return handler

def setup_logging(log_level: LogLevel) -> None:
    """ Configure le logging une seule fois par processus. Les appels suivants sont ignorés. """
    
    global _configured

    with _config_lock:
        if _configured:
            return
        
        level = getattr(logging, log_level)

        LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        #logger = logging.getLogger("app")
        logger = logging.getLogger()
        logger.setLevel(level)
        #logger.propagate = False
        
        # stdout
        logger.addHandler(
            create_stream_handler(level)
        )

        # log texte
        logger.addHandler(
            create_file_handler(
                path=LOG_FILES["text"],
                level=level,
                formatter=get_text_formatter(),
            )
        )

        # log JSON
        logger.addHandler(
            create_file_handler(
                path=LOG_FILES["json"],
                level=level,
                formatter=get_json_formatter(),
            )
        )

        _configured = True

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)