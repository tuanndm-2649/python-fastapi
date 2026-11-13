"""API routes for projects."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from demo_fastapi.crud.projects import get_projects
from demo_fastapi.database import get_db
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.projects import ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    "", response_model=PageResponse[ProjectResponse], summary="Get list projects"
)
def list_projects(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
):
    return get_projects(db, pagination)
