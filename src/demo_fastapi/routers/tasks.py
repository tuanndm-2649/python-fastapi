"""API routes for tasks."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from demo_fastapi.crud.tasks import get_tasks
from demo_fastapi.database import get_db
from demo_fastapi.models.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.tasks import TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=PageResponse[TaskResponse])
def list_users(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
):
    items, total = get_tasks(db, pagination)

    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "page_size": pagination.page_size,
    }
