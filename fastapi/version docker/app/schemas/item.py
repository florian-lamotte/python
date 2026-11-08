from pydantic import BaseModel, ConfigDict

class ItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: int
    item_name: str | None = None