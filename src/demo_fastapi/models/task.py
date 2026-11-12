from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from demo_fastapi.database import Base
from demo_fastapi.models.associations import task_tags

if TYPE_CHECKING:
    from demo_fastapi.models.comment import Comment
    from demo_fastapi.models.project import Project
    from demo_fastapi.models.tag import Tag
    from demo_fastapi.models.user import User


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'done')", name="ck_tasks_status"
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(20),
        default="todo",
        server_default="todo",
    )
    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id"),
        index=True,
    )
    assignee_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)

    project: Mapped[Project] = relationship(back_populates="tasks")
    assignee: Mapped[User | None] = relationship(back_populates="assigned_tasks")
    comments: Mapped[list[Comment]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )
    tags: Mapped[list[Tag]] = relationship(secondary=task_tags, back_populates="tasks")
