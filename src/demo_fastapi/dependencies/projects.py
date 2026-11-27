"""Dependencies for routes that require an existing project."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from demo_fastapi.common.permissions import is_admin_or_owner
from demo_fastapi.constants.message import NOT_PROJECT_MANAGER, PROJECT_NOT_FOUND
from demo_fastapi.crud.projects import get_project
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.auth import get_current_active_user
from demo_fastapi.exceptions import ForbiddenException, NotFoundException
from demo_fastapi.models import Project, User


def get_project_detail(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> Project:
    project = get_project(db, project_id)

    if project is None:
        raise NotFoundException(PROJECT_NOT_FOUND)

    return project


def verify_project_manager(
    user: Annotated[User, Depends(get_current_active_user)],
    project: Annotated[Project, Depends(get_project_detail)],
) -> Project:
    if not is_admin_or_owner(user, project.owner_id):
        raise ForbiddenException(NOT_PROJECT_MANAGER)

    return project
