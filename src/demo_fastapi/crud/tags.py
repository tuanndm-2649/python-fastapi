"""Database operations for tags."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.models import Tag


def get_tags(db: Session) -> list[Tag]:
    statement = select(Tag).order_by(Tag.id)

    return list(db.scalars(statement).all())
