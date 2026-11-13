"""API routes for projects."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from demo_fastapi.crud.projects import get_project, get_projects
from demo_fastapi.database import get_db
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.projects import ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=PageResponse[ProjectResponse], summary="List projects")
def list_projects(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
) -> PageResponse[ProjectResponse]:
    return get_projects(db, pagination)


@router.get("/{project_id}", response_model=ProjectResponse, summary="Project detail")
def retrieve_project(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> ProjectResponse:
    project = get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectResponse.model_validate(project)
