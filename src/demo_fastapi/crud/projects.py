"""Database operations for projects."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import Project
from demo_fastapi.models.pagination import PaginationParams


def get_projects(
    db: Session, pagination: PaginationParams
) -> tuple[list[Project], int]:
    statement = select(Project).order_by(Project.id)

    return paginate(db, statement, pagination)
