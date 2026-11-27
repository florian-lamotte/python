from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.schemas.item import ItemCreate, ItemResponse
from app.types.item import ItemId, ItemServiceDep
from app.models.item import Item
from app.core.database.database import get_db

router = APIRouter(
    prefix="/items", 
    tags=["Items"]
)

@router.get(
    "/read-item/{item_id}", 
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

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Connexion à PostgreSQL configurée"}

@router.post("/create_item", response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    new_item = Item(name=item.name)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@router.get("/get_item/{test_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Item introuvable"
        )

    return item

@router.get("/get_items", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()

    return items