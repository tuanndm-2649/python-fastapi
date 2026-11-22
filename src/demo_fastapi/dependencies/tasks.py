from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import NOT_PROJECT_MANAGER, TASK_NOT_FOUND
from demo_fastapi.constants.user import UserRole
from demo_fastapi.crud.tasks import get_task
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.auth import get_current_active_user
from demo_fastapi.exceptions import ForbiddenException, NotFoundException
from demo_fastapi.models import Task, User


def get_task_detail(task_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Task:
    task = get_task(db, task_id)

    if task is None:
        raise NotFoundException(TASK_NOT_FOUND)

    return task


def verify_task_manager(
    user: Annotated[User, Depends(get_current_active_user)],
    task: Annotated[Task, Depends(get_task_detail)],
) -> Task:
    if not (user.role == UserRole.ADMIN or task.project.owner_id == user.id):
        raise ForbiddenException(NOT_PROJECT_MANAGER)

    return task
