import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from threading import Lock

from app.core.config import LogLevel
from app.core.request_context import request_id_var

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

class RequestIdFilter(logging.Filter):
    """ Ajoute l'id de la requête dans les logs """
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True

_configured = False
_config_lock = Lock()

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
        
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s "
            "- request_id=%(request_id)s "
            "- %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        
        file_handler = TimedRotatingFileHandler(
            LOG_FILE,
            when="midnight", # utilise l'heure locale de la machine
            interval=1,
            backupCount=0, # nombre de fichiers max conservés
            encoding="utf-8",
            utc=True,
        )
        
        file_handler.setLevel(level)
        file_handler.addFilter(RequestIdFilter())
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)

        _configured = True

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)