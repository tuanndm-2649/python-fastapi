"""Responses combining schemas from multiple resources."""

from typing import Any
from uuid import UUID

from fastapi import status
from pydantic import BaseModel, ConfigDict

from demo_fastapi.schemas.pagination import PageResponse
from demo_fastapi.schemas.projects import ProjectResponse
from demo_fastapi.schemas.tasks import TaskResponse


class ProjectWithTasksResponse(ProjectResponse):
    tasks: PageResponse[TaskResponse]


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    username: str
    projects: list[ProjectResponse]


class ErrorResponse(BaseModel):
    detail: str


def not_found_response(message: str) -> dict[int | str, dict[str, Any]]:
    return {
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": message,
        }
    }
