"""API routes for tasks."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import (
    ERROR_TASK_BOOKMARKED,
    INVALID_TOKEN,
    TASK_NOT_FOUND,
    USER_INACTIVE,
)
from demo_fastapi.constants.task import TaskPriority, TaskStatus
from demo_fastapi.crud.tasks import create_task_bookmark, get_tasks
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.auth import get_current_active_user
from demo_fastapi.dependencies.tasks import get_task_detail
from demo_fastapi.exceptions import ConflictException
from demo_fastapi.models import Task, User
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.responses import error_response, not_found_response
from demo_fastapi.schemas.tasks import TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=PageResponse[TaskResponse], summary="Get list task")
def list_tasks(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    priority: Annotated[TaskPriority | None, Query()] = None,
) -> PageResponse[TaskResponse]:
    return get_tasks(db, pagination, task_status, priority)


@router.post(
    "/{task_id}/bookmark",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Bookmark task",
    responses={
        **error_response(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN),
        **error_response(status.HTTP_403_FORBIDDEN, USER_INACTIVE),
        **error_response(status.HTTP_409_CONFLICT, ERROR_TASK_BOOKMARKED),
        **not_found_response(TASK_NOT_FOUND),
    },
)
def bookmark_task(
    db: Annotated[Session, Depends(get_db)],
    task: Annotated[Task, Depends(get_task_detail)],
    user: Annotated[User, Depends(get_current_active_user)],
) -> Task:
    try:
        return create_task_bookmark(db, user, task)
    except IntegrityError:
        raise ConflictException(ERROR_TASK_BOOKMARKED)
