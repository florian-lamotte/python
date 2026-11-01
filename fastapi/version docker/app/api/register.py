from fastapi import FastAPI

from app.api.router import api_router

def register_routers(app: FastAPI) -> None:
    app.include_router(api_router)