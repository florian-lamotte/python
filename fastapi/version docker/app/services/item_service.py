from app.schemas.item import ItemResponse

class ItemService:
    def get_item(
        self,
        item_id: int, 
        name: str | None = None,
    ) -> ItemResponse:
        return ItemResponse(item_id=item_id, name=name)
    
    #def create_item(self, item_data):

    #def update_item(self, item_id: int, item_data):

    #def delete_item(self, item_id: int):