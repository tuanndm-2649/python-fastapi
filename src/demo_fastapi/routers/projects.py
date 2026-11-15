"""API routes for projects."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from demo_fastapi.common.validators import get_tags_or_404, get_user_or_404
from demo_fastapi.crud.projects import get_projects
from demo_fastapi.crud.tasks import create_task, get_tasks_by_project
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.projects import get_project_or_404
from demo_fastapi.models import Project, Task
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.projects import ProjectResponse
from demo_fastapi.schemas.responses import ProjectWithTasksResponse
from demo_fastapi.schemas.tasks import TaskCreate, TaskResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=PageResponse[ProjectResponse], summary="List projects")
def list_projects(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
) -> PageResponse[ProjectResponse]:
    return get_projects(db, pagination)


@router.get("/{project_id}", response_model=ProjectResponse, summary="Project detail")
def retrieve_project(
    project: Annotated[Project, Depends(get_project_or_404)],
) -> ProjectResponse:
    return ProjectResponse.model_validate(project)


@router.get(
    "/{project_id}/tasks",
    response_model=ProjectWithTasksResponse,
    summary="Tasks by project",
)
def get_project_with_tasks(
    project: Annotated[Project, Depends(get_project_or_404)],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
) -> ProjectWithTasksResponse:
    project_data = ProjectResponse.model_validate(project)
    task_data = get_tasks_by_project(db, pagination, project.id)

    return ProjectWithTasksResponse(**project_data.model_dump(), tasks=task_data)


@router.post(
    "/{project_id}/tasks", response_model=TaskResponse, summary="Create task project"
)
def create_project_task(
    project: Annotated[Project, Depends(get_project_or_404)],
    db: Annotated[Session, Depends(get_db)],
    payload: TaskCreate,
) -> Task:
    if payload.assignee_id is not None:
        get_user_or_404(db, payload.assignee_id)

    tags = get_tags_or_404(db, payload.tags)

    return create_task(db, payload, project.id, tags)
