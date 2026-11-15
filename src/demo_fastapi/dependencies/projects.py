"""Dependencies for routes that require an existing project."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from demo_fastapi.common.validators import get_project_or_404 as validate_project
from demo_fastapi.database import get_db
from demo_fastapi.models import Project


def get_project_or_404(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> Project:
    return validate_project(db, project_id)
