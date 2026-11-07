from typing import Annotated
from fastapi import Depends, Path

from app.services.item_service import ItemService
from app.core.dependencies.item_dependencies import get_item_service

ItemId = Annotated[
    int, Path(
        gt=0, 
        description="Identifiant unique de l'item",
    ),
]

ItemServiceDep = Annotated[
    ItemService,
    Depends(get_item_service),
]