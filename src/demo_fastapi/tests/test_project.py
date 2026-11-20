from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import (
    NOT_PROJECT_MANAGER,
    PROJECT_NOT_FOUND,
    TAGS_NOT_FOUND,
    USER_INACTIVE,
    USER_NOT_FOUND,
)
from demo_fastapi.models import Project, Tag, Task, User
from demo_fastapi.tests.test_users import (
    deactivate_user,
    get_auth_headers,
    make_auth_headers,
)

PROJECT_ID = UUID(int=1)
UNKNOWN_ID = UUID(int=999)


def seed_project(db_session: Session) -> Project:
    owner = User(
        name="Owner",
        username="owner",
        email="owner@example.com",
        hashed_password="test-only",
    )
    project = Project(id=PROJECT_ID, name="Project 1", owner=owner)
    db_session.add_all([owner, project])
    db_session.commit()

    return project


def sign_token_for_owner(project: Project) -> dict[str, str]:
    return make_auth_headers(
        {"sub": str(project.owner_id), "exp": datetime.now(UTC) + timedelta(minutes=5)}
    )


def test_project_detail_returns_200(client: TestClient, db_session: Session) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.get(f"/api/projects/{PROJECT_ID}", headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Project 1"


def test_project_detail_not_found_returns_404(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.get(f"/api/projects/{UNKNOWN_ID}", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == PROJECT_NOT_FOUND


def test_project_detail_invalid_id_returns_422(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.get("/api/projects/abc", headers=headers)

    assert response.status_code == 422


# Create task


def test_create_task_returns_201(client: TestClient, db_session: Session) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks",
        json={"title": "Task 1"},
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Task 1"
    assert data["assignee"] is None
    assert data["tags"] == []


def test_create_task_with_assignee_and_tags_returns_201(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)
    tag = Tag(name="bug")
    db_session.add(tag)
    db_session.commit()

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks",
        json={
            "title": "Task 1",
            "assignee_id": str(project.owner_id),
            "tag_ids": [str(tag.id)],
        },
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["assignee"]["id"] == str(project.owner_id)
    assert [item["name"] for item in data["tags"]] == ["bug"]


def test_create_task_with_unknown_assignee_returns_404(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks",
        json={"title": "Task 1", "assignee_id": str(UNKNOWN_ID)},
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND


def test_create_task_with_unknown_tag_returns_404(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks",
        json={"title": "Task 1", "tag_ids": [str(UNKNOWN_ID)]},
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == TAGS_NOT_FOUND.format(tag_ids=UNKNOWN_ID)


def test_create_task_with_empty_title_returns_422(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks", json={"title": ""}, headers=headers
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


# Project tasks pagination


def seed_project_tasks(db_session: Session) -> None:
    project = seed_project(db_session)

    for index in range(1, 4):
        db_session.add(Task(id=UUID(int=index), title=f"Task {index}", project=project))

    db_session.commit()


def test_project_tasks_pagination_returns_correct_total(
    client: TestClient, db_session: Session
) -> None:
    seed_project_tasks(db_session)

    response = client.get(
        f"/api/projects/{PROJECT_ID}/tasks", params={"page": 2, "page_size": 2}
    )

    assert response.status_code == 200
    tasks = response.json()["tasks"]
    assert tasks["total"] == 3
    assert [task["title"] for task in tasks["items"]] == ["Task 3"]


def test_create_task_without_token_returns_401(
    client: TestClient, db_session: Session
) -> None:
    seed_project(db_session)

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks", json={"title": "Task 1"}
    )

    assert response.status_code == 401


def test_create_task_not_owner_returns_403(
    client: TestClient, db_session: Session
) -> None:
    seed_project(db_session)
    headers = get_auth_headers(client)

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks", json={"title": "Task 1"}, headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == NOT_PROJECT_MANAGER


def test_create_task_inactive_owner_returns_403(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)
    deactivate_user(db_session, "owner")

    response = client.post(
        f"/api/projects/{PROJECT_ID}/tasks", json={"title": "Task 1"}, headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == USER_INACTIVE


def test_create_task_unknown_project_returns_404(
    client: TestClient, db_session: Session
) -> None:
    project = seed_project(db_session)
    headers = sign_token_for_owner(project)

    response = client.post(
        f"/api/projects/{UNKNOWN_ID}/tasks", json={"title": "Task 1"}, headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == PROJECT_NOT_FOUND
