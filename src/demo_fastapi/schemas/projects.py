"""Request and response schemas for projects."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from demo_fastapi.constants.project import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_NAME_MIN_LENGTH,
)


class ProjectBase(BaseModel):
    name: str = Field(
        min_length=PROJECT_NAME_MIN_LENGTH, max_length=PROJECT_NAME_MAX_LENGTH
    )
    description: str | None = None


class ProjectCreate(ProjectBase):
    owner_id: UUID


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
