"""API routes for tasks."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from demo_fastapi.common.validators import get_user_detail
from demo_fastapi.constants.message import (
    ASSIGNEE_INACTIVE,
    COMMENT_NOT_FOUND,
    ERROR_TASK_BOOKMARKED,
    INVALID_TOKEN,
    NOT_COMMENT_OWNER,
    NOT_PROJECT_MANAGER,
    TASK_NOT_FOUND,
    USER_INACTIVE,
)
from demo_fastapi.constants.task import TaskPriority, TaskStatus
from demo_fastapi.crud.comments import create_comment, delete_comment, update_comment
from demo_fastapi.crud.tasks import (
    assign_task,
    create_task_bookmark,
    get_tasks,
)
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.auth import get_current_active_user
from demo_fastapi.dependencies.comments import verify_comment_permission
from demo_fastapi.dependencies.tasks import get_task_detail, verify_task_manager
from demo_fastapi.exceptions import (
    BadRequestException,
    ConflictException,
)
from demo_fastapi.models import Comment, Task, User
from demo_fastapi.schemas.comments import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.responses import error_response, not_found_response
from demo_fastapi.schemas.tasks import TaskAssign, TaskResponse
from demo_fastapi.services import email as email_service

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


@router.post(
    "/{task_id}/assign",
    response_model=TaskResponse,
    summary="Assign task",
    responses={
        **not_found_response(TASK_NOT_FOUND),
        **error_response(status.HTTP_403_FORBIDDEN, NOT_PROJECT_MANAGER),
        **error_response(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN),
        **error_response(status.HTTP_400_BAD_REQUEST, ASSIGNEE_INACTIVE),
    },
)
def assign_user_task(
    db: Annotated[Session, Depends(get_db)],
    task: Annotated[Task, Depends(verify_task_manager)],
    payload: TaskAssign,
) -> Task:
    assignee = get_user_detail(db, payload.assignee_id)

    if not assignee.is_active:
        raise BadRequestException(ASSIGNEE_INACTIVE)

    return assign_task(db, task, assignee)


@router.post(
    "/{task_id}/comments",
    response_model=CommentResponse,
    summary="Comment task",
    status_code=status.HTTP_201_CREATED,
    responses={
        **not_found_response(TASK_NOT_FOUND),
        **error_response(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN),
        **error_response(status.HTTP_403_FORBIDDEN, USER_INACTIVE),
    },
)
def comment_on_task(
    background_tasks: BackgroundTasks,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
    task: Annotated[Task, Depends(get_task_detail)],
    payload: CommentCreate,
) -> Comment:
    to_email = task.project.owner.email
    task_title = task.title
    author_name = user.name

    comment = create_comment(db, payload, task, user)
    background_tasks.add_task(
        email_service.send_comment_notification,
        to_email=to_email,
        task_title=task_title,
        author_name=author_name,
        content=comment.content,
    )

    return comment


@router.delete(
    "/{task_id}/comments/{comment_id}",
    summary="Delete comment",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **not_found_response(COMMENT_NOT_FOUND),
        **error_response(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN),
        **error_response(status.HTTP_403_FORBIDDEN, NOT_COMMENT_OWNER),
    },
)
def delete_comment_task(
    db: Annotated[Session, Depends(get_db)],
    comment: Annotated[Comment, Depends(verify_comment_permission)],
) -> None:
    delete_comment(db, comment)


@router.patch(
    "/{task_id}/comments/{comment_id}",
    summary="Update comment",
    responses={
        **not_found_response(COMMENT_NOT_FOUND),
        **error_response(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN),
        **error_response(status.HTTP_403_FORBIDDEN, NOT_COMMENT_OWNER),
    },
    response_model=CommentResponse,
)
def update_user_comment(
    db: Annotated[Session, Depends(get_db)],
    comment: Annotated[Comment, Depends(verify_comment_permission)],
    payload: CommentUpdate,
) -> Comment:
    return update_comment(db, comment, payload)
