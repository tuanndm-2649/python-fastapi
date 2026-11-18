"""API routes for projects."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from demo_fastapi.common.validators import get_task_tags, get_user_detail
from demo_fastapi.constants.message import PROJECT_NOT_FOUND, RESOURCE_NOT_FOUND
from demo_fastapi.crud.projects import get_projects
from demo_fastapi.crud.tasks import create_task, get_tasks_by_project
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.projects import get_project_detail
from demo_fastapi.models import Project, Task
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.projects import ProjectResponse
from demo_fastapi.schemas.responses import ProjectWithTasksResponse, not_found_response
from demo_fastapi.schemas.tasks import TaskCreate, TaskResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=PageResponse[ProjectResponse], summary="List projects")
def list_projects(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
) -> PageResponse[ProjectResponse]:
    return get_projects(db, pagination)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Project detail",
    responses=not_found_response(PROJECT_NOT_FOUND),
)
def retrieve_project(
    project: Annotated[Project, Depends(get_project_detail)],
) -> ProjectResponse:
    return ProjectResponse.model_validate(project)


@router.get(
    "/{project_id}/tasks",
    response_model=ProjectWithTasksResponse,
    summary="Tasks by project",
    responses=not_found_response(PROJECT_NOT_FOUND),
)
def get_project_with_tasks(
    project: Annotated[Project, Depends(get_project_detail)],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
) -> ProjectWithTasksResponse:
    project_data = ProjectResponse.model_validate(project)
    task_data = get_tasks_by_project(db, pagination, project.id)

    return ProjectWithTasksResponse(**project_data.model_dump(), tasks=task_data)


@router.post(
    "/{project_id}/tasks",
    response_model=TaskResponse,
    summary="Create task project",
    status_code=status.HTTP_201_CREATED,
    responses=not_found_response(RESOURCE_NOT_FOUND),
)
def create_project_task(
    project: Annotated[Project, Depends(get_project_detail)],
    db: Annotated[Session, Depends(get_db)],
    payload: TaskCreate,
) -> Task:
    if payload.assignee_id is not None:
        get_user_detail(db, payload.assignee_id)

    tags = get_task_tags(db, payload.tag_ids)

    return create_task(db, payload, project.id, tags)
