"""Dependencies for routes that require an existing project."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import PROJECT_NOT_FOUND
from demo_fastapi.crud.projects import get_project
from demo_fastapi.database import get_db
from demo_fastapi.exceptions import NotFoundException
from demo_fastapi.models import Project


def get_project_detail(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> Project:
    project = get_project(db, project_id)

    if project is None:
        raise NotFoundException(PROJECT_NOT_FOUND)

    return project
