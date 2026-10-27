from fastapi import APIRouter
from app.schemas.item import ItemResponse
from app.services.item_service import get_item

router = APIRouter(prefix="/items", tags=["Items"])

@router.get(
    "/{item_id}",
    response_model=ItemResponse,
)
def read_item(
    item_id: int,
    q: str | None = None,
) -> ItemResponse:
    return get_item(item_id, q)