"""Database operations for projects."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import Project
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.projects import ProjectResponse


def get_projects(
    db: Session, pagination: PaginationParams
) -> PageResponse[ProjectResponse]:
    statement = select(Project).order_by(Project.id)

    return paginate(db, statement, pagination, PageResponse[ProjectResponse])
