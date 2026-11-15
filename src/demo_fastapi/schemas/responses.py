"""Responses combining schemas from multiple resources."""

from demo_fastapi.schemas.pagination import PageResponse
from demo_fastapi.schemas.projects import ProjectResponse
from demo_fastapi.schemas.tasks import TaskResponse
from demo_fastapi.schemas.users import UserResponse


class ProjectWithTasksResponse(ProjectResponse):
    tasks: PageResponse[TaskResponse]


class UserProfileResponse(UserResponse):
    username: str
    projects: list[ProjectResponse]
