from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from demo_fastapi.database import Base

if TYPE_CHECKING:
    from demo_fastapi.models.task import Task
    from demo_fastapi.models.user import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    content: Mapped[str] = mapped_column(Text)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), index=True)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)

    task: Mapped[Task] = relationship(back_populates="comments")
    author: Mapped[User] = relationship(back_populates="comments")
