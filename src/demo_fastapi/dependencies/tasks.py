from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import TASK_NOT_FOUND
from demo_fastapi.crud.tasks import get_task
from demo_fastapi.database import get_db
from demo_fastapi.exceptions import NotFoundException
from demo_fastapi.models import Task


def get_task_detail(task_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Task:
    task = get_task(db, task_id)

    if task is None:
        raise NotFoundException(TASK_NOT_FOUND)

    return task
