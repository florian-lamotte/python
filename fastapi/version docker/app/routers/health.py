from fastapi import APIRouter

router = APIRouter(tags=["Monitoring"])

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/ready")
async def readiness():
    return {"status": "ready"}