"""Database operations for tasks."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import Task
from demo_fastapi.models.pagination import PaginationParams


def get_tasks(db: Session, pagination: PaginationParams) -> tuple[list[Task], int]:
    statement = select(Task).order_by(Task.id)

    return paginate(db, statement, pagination)
