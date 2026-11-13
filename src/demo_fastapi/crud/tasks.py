"""Database operations for tasks."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import Task
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.tasks import TaskResponse


def get_tasks(db: Session, pagination: PaginationParams) -> PageResponse[TaskResponse]:
    statement = select(Task).order_by(Task.id)

    return paginate(db, statement, pagination, response_type=PageResponse[TaskResponse])
