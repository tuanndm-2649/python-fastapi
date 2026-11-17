from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from demo_fastapi.models import Project, User


def test_project_detail_returns_200(client: TestClient, db_session: Session) -> None:
    owner = User(name="Owner", email="owner@example.com", hashed_password="test-only")
    project = Project(id=UUID(int=1), name="project 1", owner=owner)

    db_session.add_all([owner, project])
    db_session.commit()

    response = client.get(f"/api/projects/{UUID(int=1)}")

    assert response.status_code == 200
    assert response.json()["name"] == "project 1"


def test_project_detail_not_found_returns_404(client: TestClient) -> None:
    response = client.get(f"/api/projects/{UUID(int=900)}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_project_detail_invalid_id_returns_422(client: TestClient) -> None:
    response = client.get("/api/projects/abc")

    assert response.status_code == 422
