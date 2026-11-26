from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.schemas.item import ItemResponse
from app.types.item import ItemId, ItemServiceDep
from app.core.database.database import get_db

router = APIRouter(
    prefix="/items", 
    tags=["Items"]
)

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Connexion à PostgreSQL configurée"}

@router.get(
    "/{item_id}", 
    response_model=ItemResponse,
    summary="Retourne un item",
    description="Retourne un item à partir de son identifiant.",
)
def read_item(
    item_id: ItemId,
    item_service: ItemServiceDep,
    item_name: Annotated[
        str | None,
        Query(
            max_length=100, 
            description="Paramètre optionnel",
        ),
    ] = None,
) -> ItemResponse:
    return item_service.get_item(
        item_id, 
        item_name
    )