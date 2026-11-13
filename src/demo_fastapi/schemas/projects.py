"""Request and response schemas for projects."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    owner_id: UUID
