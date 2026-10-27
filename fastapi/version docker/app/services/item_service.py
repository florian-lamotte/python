from app.schemas.item import ItemResponse

def get_item(
    item_id: int,
    q: str | None = None,
) -> ItemResponse:
    return ItemResponse(item_id=item_id, q=q)