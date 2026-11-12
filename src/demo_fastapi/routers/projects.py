"""API routes for projects."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from demo_fastapi.crud.projects import get_projects
from demo_fastapi.database import get_db
from demo_fastapi.models.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.projects import ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=PageResponse[ProjectResponse])
def list_project(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
):
    items, total = get_projects(db, pagination)

    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "page_size": pagination.page_size,
    }
