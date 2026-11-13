import time
import uuid

from fastapi import Request
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from app.core.logging_config import get_logger
from app.core.request_context import request_id_var

logger = get_logger(__name__)

async def log_requests(
    request: Request, 
    call_next: RequestResponseEndpoint,
) -> Response:
    request_id = str(uuid.uuid4()) # Génération d'un UUID unique pour chaque requête
    token = request_id_var.set(request_id) # Place l'identifiant dans le ContextVar
    
    start_time = time.perf_counter()
    
    method = request.method
    path = request.url.path
    
    # Transmet les requêtes au middleware avec des niveaux de logs adaptés
    try:
        # request.state.request_id peut être accédé par d'autres composants FastAPI pour retrouver l'identifiant
        request.state.request_id = request_id
        
        response = await call_next(request)
        
        duration = time.perf_counter() - start_time
        status_code = response.status_code

        response.headers["X-Request-ID"] = request_id
        
        message = "%s %s - status=%s - duration=%.3fs"
        
        if status_code >= 500:
            logger.error(message, method, path, status_code, duration)
        elif status_code >= 400:
            logger.warning(message, method, path, status_code, duration)
        else:
            logger.info(message, method, path, status_code, duration)
        
        return response
    # Enregistre les exceptions dans les logs pour ne pas rater d'erreur 
    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "%s %s - exception - duration=%.3fs",
            method,
            path,
            duration,
        )
        
        raise
    finally:
        # Réinitialiste le ContextVar
        request_id_var.reset(token)