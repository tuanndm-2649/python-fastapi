from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from demo_fastapi.crud.users import get_users
from demo_fastapi.database import get_db
from demo_fastapi.models.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.users import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PageResponse[UserResponse])
def list_users(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
):
    items, total = get_users(db, pagination)

    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "page_size": pagination.page_size,
    }
