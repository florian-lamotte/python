from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from app.schemas.item import ItemResponse
from app.services.item_service import ItemService
from app.core.dependencies.item_dependencies import get_item_service

router = APIRouter(prefix="/items", tags=["Items"])

@router.get(
    "/{item_id}", 
    response_model=ItemResponse,
    summary="Retourne un item",
    description="Retourne un item à partir de son identifiant obligatoire.",
)
async def read_item(
    item_id: Annotated[int, Path(gt=0)], 
    name: Annotated[str | None, Query(max_length=100)] = None,
    item_service: Annotated[ItemService, Depends(get_item_service)] = None,
) -> ItemResponse:
    return item_service.get_item(item_id, name)