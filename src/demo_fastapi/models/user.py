from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from demo_fastapi.database import Base

if TYPE_CHECKING:
    from demo_fastapi.models.comment import Comment
    from demo_fastapi.models.project import Project
    from demo_fastapi.models.task import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    projects: Mapped[list[Project]] = relationship(
        back_populates="owner",
    )
    assigned_tasks: Mapped[list[Task]] = relationship(back_populates="assignee")
    comments: Mapped[list[Comment]] = relationship(back_populates="author")
