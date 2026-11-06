from fastapi import APIRouter

router = APIRouter(tags=["Monitoring"])

@router.get("/health", summary="Etat de FastAPI",)
async def health():
    return {"status": "ok"}

@router.get("/ready", summary="",)
async def readiness():
    return {"status": "ready"}