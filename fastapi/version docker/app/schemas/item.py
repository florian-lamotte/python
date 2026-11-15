from pydantic import BaseModel, ConfigDict, Field

class ItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: int = Field(gt=0)
    item_name: str | None = None