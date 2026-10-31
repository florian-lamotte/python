from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Divers"])
async def read_root():
    return {"message": "Bonjour"}