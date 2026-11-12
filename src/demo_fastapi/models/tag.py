from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from demo_fastapi.database import Base
from demo_fastapi.models.associations import task_tags

if TYPE_CHECKING:
    from demo_fastapi.models.task import Task


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )

    tasks: Mapped[list[Task]] = relationship(secondary=task_tags, back_populates="tags")
