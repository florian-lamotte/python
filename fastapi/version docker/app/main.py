from fastapi import FastAPI
from app.routers import items

app = FastAPI(
    title="API",
    description="Prototype d'API",
    version="0.1.0",
)

@app.get("/", tags=["Divers"])
def read_root():
    return {"message": "Bonjour"}

app.include_router(items.router)