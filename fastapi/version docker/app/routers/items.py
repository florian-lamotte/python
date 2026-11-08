from typing import Annotated
from fastapi import APIRouter, Query

from app.schemas.item import ItemResponse
from app.core.types.item import ItemId, ItemServiceDep

router = APIRouter(prefix="/items", tags=["Items"])

@router.get(
    "/{item_id}", 
    response_model=ItemResponse,
    summary="Retourne un item",
    description="Retourne un item à partir de son identifiant obligatoire.",
)
async def read_item(
    item_id: ItemId,
    item_service: ItemServiceDep,
    item_name: Annotated[
        str | None,
        Query(max_length=100, description="Paramètre optionnel",),
    ] = None,
) -> ItemResponse:
    return item_service.get_item(item_id, item_name)