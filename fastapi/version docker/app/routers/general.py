from fastapi import APIRouter

router = APIRouter(tags=["Divers"])

@router.get("/")
async def read_root():
    return {"message": "Bonjour"}