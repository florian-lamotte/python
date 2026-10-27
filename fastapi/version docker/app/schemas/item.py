from pydantic import BaseModel, ConfigDict

class ItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: int
    q: str | None = None