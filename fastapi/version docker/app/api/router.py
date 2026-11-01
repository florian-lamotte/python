from fastapi import APIRouter
from app.routers import general, health, items

api_router = APIRouter()

api_router.include_router(general.router)
api_router.include_router(health.router)
api_router.include_router(items.router)