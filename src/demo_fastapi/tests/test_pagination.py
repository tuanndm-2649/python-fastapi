from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from demo_fastapi.models import Project, Task, User


def seed_users(db_session: Session) -> None:
    for index in range(1, 4):
        user = User(
            id=UUID(int=index),
            name=f"User {index}",
            email=f"user{index}@example.com",
            hashed_password="test-only",
        )
        db_session.add(user)

    db_session.commit()


def seed_projects(db_session: Session) -> None:
    owner = User(
        name="Project owner",
        email="owner@example.com",
        hashed_password="test-only",
    )
    db_session.add(owner)

    for index in range(1, 4):
        project = Project(
            id=UUID(int=index),
            name=f"Project {index}",
            owner=owner,
        )
        db_session.add(project)

    db_session.commit()


def seed_tasks(db_session: Session) -> None:
    owner = User(
        name="Task owner",
        email="owner@example.com",
        hashed_password="test-only",
    )
    project = Project(name="Test project", owner=owner)
    db_session.add_all([owner, project])

    for index in range(1, 4):
        task = Task(
            id=UUID(int=index),
            title=f"Task {index}",
            project=project,
        )
        db_session.add(task)

    db_session.commit()


# Users


def test_users_page_zero_returns_422(client: TestClient) -> None:
    response = client.get("/api/users", params={"page": 0})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "page"]


def test_users_pagination_returns_correct_total(
    client: TestClient, db_session: Session
) -> None:
    seed_users(db_session)

    response = client.get("/api/users", params={"page": 2, "page_size": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total_pages"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(UUID(int=3))


def test_users_page_beyond_last_page_returns_empty_items(
    client: TestClient, db_session: Session
) -> None:
    seed_users(db_session)

    response = client.get("/api/users", params={"page": 3, "page_size": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 3
    assert data["total_pages"] == 2


# Projects


def test_projects_page_zero_returns_422(client: TestClient) -> None:
    response = client.get("/api/projects", params={"page": 0})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "page"]


def test_projects_pagination_returns_correct_total(
    client: TestClient, db_session: Session
) -> None:
    seed_projects(db_session)

    response = client.get("/api/projects", params={"page": 2, "page_size": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total_pages"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(UUID(int=3))


def test_projects_page_beyond_last_page_returns_empty_items(
    client: TestClient, db_session: Session
) -> None:
    seed_projects(db_session)

    response = client.get("/api/projects", params={"page": 3, "page_size": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 3
    assert data["total_pages"] == 2


# Tasks


def test_tasks_page_zero_returns_422(client: TestClient) -> None:
    response = client.get("/api/tasks", params={"page": 0})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "page"]


def test_tasks_pagination_returns_correct_total(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)

    response = client.get("/api/tasks", params={"page": 2, "page_size": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total_pages"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(UUID(int=3))


def test_tasks_page_beyond_last_page_returns_empty_items(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)

    response = client.get("/api/tasks", params={"page": 3, "page_size": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 3
    assert data["total_pages"] == 2
