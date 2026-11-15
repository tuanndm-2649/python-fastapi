"""Request and response schemas for tasks."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from demo_fastapi.constants.task import (
    TASK_TITLE_MAX_LENGTH,
    TASK_TITLE_MIN_LENGTH,
    TaskStatus,
)
from demo_fastapi.schemas.projects import ProjectResponse
from demo_fastapi.schemas.tags import TagResponse
from demo_fastapi.schemas.users import UserResponse


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    project: ProjectResponse
    assignee: UserResponse | None
    tags: list[TagResponse]


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=TASK_TITLE_MIN_LENGTH, max_length=TASK_TITLE_MAX_LENGTH
    )
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    assignee_id: UUID | None = None
    tags: list[UUID] = Field(default_factory=list)
