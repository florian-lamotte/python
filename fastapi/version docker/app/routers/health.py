from fastapi import APIRouter, Response, status

from app.schemas.health import HealthResponse

router = APIRouter(tags=["Monitoring"])

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")

@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Readiness check",
)
async def readiness(response: Response,) -> HealthResponse:
    # placeholder à remplacer par une vérification des dépendances
    is_ready = True

    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(status="not ready")
    
    return HealthResponse(status="ready")