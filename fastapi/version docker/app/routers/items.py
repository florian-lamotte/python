from fastapi import APIRouter, Depends
from app.schemas.item import ItemResponse
from app.services.item_service import ItemService
from app.core.dependencies.item_dependencies import get_item_service

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int, 
    q: str | None = None,
    item_service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    return item_service.get_item(item_id, q)