"""Database operations for tags."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.models import Tag


def get_tags(db: Session) -> list[Tag]:
    statement = select(Tag).order_by(Tag.id)

    return list(db.scalars(statement).all())


def get_tags_by_ids(db: Session, tag_ids: list[UUID]) -> list[Tag]:
    statement = select(Tag).where(Tag.id.in_(tag_ids)).order_by(Tag.id)

    return list(db.scalars(statement).all())
