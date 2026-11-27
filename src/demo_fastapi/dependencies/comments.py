from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from demo_fastapi.common.permissions import is_admin_or_owner
from demo_fastapi.constants.message import COMMENT_NOT_FOUND, NOT_COMMENT_OWNER
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.auth import get_current_active_user
from demo_fastapi.dependencies.tasks import get_task_detail
from demo_fastapi.exceptions import ForbiddenException, NotFoundException
from demo_fastapi.models import Comment, Task, User


def get_comment_detail(
    comment_id: UUID,
    task: Annotated[Task, Depends(get_task_detail)],
    db: Annotated[Session, Depends(get_db)],
) -> Comment:
    comment = db.get(Comment, comment_id)

    if not comment or comment.task_id != task.id:
        raise NotFoundException(COMMENT_NOT_FOUND)

    return comment


def verify_comment_permission(
    user: Annotated[User, Depends(get_current_active_user)],
    comment: Annotated[Comment, Depends(get_comment_detail)],
) -> Comment:
    is_author = comment.author_id == user.id
    is_manager = is_admin_or_owner(user, comment.task.project.owner_id)

    if not (is_author or is_manager):
        raise ForbiddenException(NOT_COMMENT_OWNER)

    return comment
