"""Database operations for tasks."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload, selectinload

from demo_fastapi.constants.task import TaskPriority, TaskStatus
from demo_fastapi.crud.pagination import paginate
from demo_fastapi.models import Tag, Task, User
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.tasks import TaskCreate, TaskResponse


def get_tasks(
    db: Session,
    pagination: PaginationParams,
    status: TaskStatus | None,
    priority: TaskPriority | None,
) -> PageResponse[TaskResponse]:
    statement = select(Task).options(
        joinedload(Task.project),
        joinedload(Task.assignee),
        selectinload(Task.tags),
    )

    if status is not None:
        statement = statement.where(Task.status == status)

    if priority is not None:
        statement = statement.where(Task.priority == priority)

    statement = statement.order_by(Task.id)

    return paginate(db, statement, pagination, response_type=PageResponse[TaskResponse])


def get_task(db: Session, task_id: UUID) -> Task | None:
    return db.get(Task, task_id)


def get_tasks_by_project(
    db: Session, pagination: PaginationParams, project_id: UUID
) -> PageResponse[TaskResponse]:
    statement = (
        select(Task)
        .where(Task.project_id == project_id)
        .options(joinedload(Task.assignee), selectinload(Task.tags))
        .order_by(Task.id)
    )

    return paginate(db, statement, pagination, response_type=PageResponse[TaskResponse])


def create_task(
    db: Session, payload: TaskCreate, project_id: UUID, tags: list[Tag]
) -> Task:
    task_data = payload.model_dump(exclude={"tag_ids"})

    task = Task(**task_data, project_id=project_id)
    task.tags = tags

    try:
        db.add(task)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(task)
    return task


def create_task_bookmark(db: Session, user: User, task: Task) -> Task:
    user.bookmarked_tasks.append(task)
    db.commit()
    db.refresh(task)

    return task
