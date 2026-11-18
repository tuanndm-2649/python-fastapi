"""Database operations for users."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from demo_fastapi.core.security import hash_password
from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import User
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.users import UserRegister, UserResponse, UserUpdate


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


def get_user_by_username(db: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)

    return db.scalars(statement).one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)

    return db.scalars(statement).one_or_none()


def create_user(db: Session, payload: UserRegister) -> User:
    user = User(
        name=payload.name,
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    user.name = payload.name
    db.commit()
    db.refresh(user)

    return user
