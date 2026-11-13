"""Request and response schemas for tasks."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: str
    project_id: UUID
    assignee_id: UUID | None
