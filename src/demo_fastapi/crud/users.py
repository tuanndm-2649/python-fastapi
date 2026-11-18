"""Database operations for users."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import User
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.users import UserResponse


def get_users(db: Session, pagination: PaginationParams) -> PageResponse[UserResponse]:
    statement = select(User).order_by(User.id)

    return paginate(db, statement, pagination, response_type=PageResponse[UserResponse])


def retrieve_user(db: Session, user_id: UUID) -> User | None:
    return db.get(User, user_id)


def get_user_profile_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = (
        select(User)
        .where(User.username == username)
        .options(
            selectinload(User.projects),
        )
    )

    return db.scalars(statement).one_or_none()
