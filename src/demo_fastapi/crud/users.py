"""Database operations for users."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import User
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.users import UserResponse


def get_users(db: Session, pagination: PaginationParams) -> PageResponse[UserResponse]:
    statement = select(User).order_by(User.id)

    return paginate(db, statement, pagination, response_type=PageResponse[UserResponse])
