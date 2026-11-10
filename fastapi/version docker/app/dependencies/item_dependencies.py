from app.services.item_service import ItemService

def get_item_service() -> ItemService:
    return ItemService()