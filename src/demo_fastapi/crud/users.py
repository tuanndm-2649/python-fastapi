"""Database operations for users."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import User
from demo_fastapi.models.pagination import PaginationParams


def get_users(db: Session, pagination: PaginationParams) -> tuple[list[User], int]:
    statement = select(User).order_by(User.id)

    return paginate(db, statement, pagination)
