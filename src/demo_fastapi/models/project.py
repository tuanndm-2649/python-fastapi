from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from demo_fastapi.database import Base

if TYPE_CHECKING:
    from demo_fastapi.models.task import Task
    from demo_fastapi.models.user import User


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)

    owner: Mapped[User] = relationship(
        "User",
        back_populates="projects",
    )
    tasks: Mapped[list[Task]] = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )
