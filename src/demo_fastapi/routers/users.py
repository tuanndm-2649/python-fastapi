from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from demo_fastapi.crud.users import get_users
from demo_fastapi.database import get_db
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.users import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PageResponse[UserResponse], summary="Get list users")
def list_users(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
) -> PageResponse[UserResponse]:
    return get_users(db, pagination)
