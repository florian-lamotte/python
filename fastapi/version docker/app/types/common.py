from typing import Annotated
from fastapi import Query

PaginationLimit = Annotated[
    int,
    Query(ge=1, le=100),
]

PaginationOffset = Annotated[
    int,
    Query(ge=0),
]

"""
from app.core.types.common import PaginationLimit, PaginationOffset

@router.get("/")
def list_items(
    limit: PaginationLimit = 20,
    offset: PaginationOffset = 0,
):
"""