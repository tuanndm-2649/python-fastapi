"""API routes for tasks."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from demo_fastapi.crud.tasks import get_tasks
from demo_fastapi.database import get_db
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.tasks import TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=PageResponse[TaskResponse], summary="Get list task")
def list_tasks(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
):
    return get_tasks(db, pagination)
