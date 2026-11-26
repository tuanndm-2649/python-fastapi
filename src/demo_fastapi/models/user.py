from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from demo_fastapi.common.utils import enum_check
from demo_fastapi.constants.user import UserRole
from demo_fastapi.database import Base
from demo_fastapi.models.associations import task_bookmarks

if TYPE_CHECKING:
    from demo_fastapi.models.comment import Comment
    from demo_fastapi.models.project import Project
    from demo_fastapi.models.task import Task


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(enum_check("role", UserRole), name="ck_users_role"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(55), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
    role: Mapped[str] = mapped_column(
        String(10), default=UserRole.USER, server_default=UserRole.USER
    )

    projects: Mapped[list[Project]] = relationship(
        back_populates="owner",
    )
    assigned_tasks: Mapped[list[Task]] = relationship(back_populates="assignee")
    comments: Mapped[list[Comment]] = relationship(back_populates="author")
    bookmarked_tasks: Mapped[list[Task]] = relationship(secondary=task_bookmarks)
