from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import (
    ERROR_TASK_BOOKMARKED,
    TASK_NOT_FOUND,
    USER_INACTIVE,
)
from demo_fastapi.constants.task import TaskPriority, TaskStatus
from demo_fastapi.models import Task, User
from demo_fastapi.tests.test_project import UNKNOWN_ID, seed_project
from demo_fastapi.tests.test_users import USER_NAME, get_auth_headers

TASK_ID = UUID(int=10)


def seed_tasks(db_session: Session) -> None:
    project = seed_project(db_session)
    db_session.add_all(
        [
            Task(
                id=TASK_ID,
                title="Task 1",
                project=project,
                status=TaskStatus.TODO,
                priority=TaskPriority.HIGH,
            ),
            Task(
                title="Task 2",
                project=project,
                status=TaskStatus.DONE,
                priority=TaskPriority.LOW,
            ),
        ]
    )
    db_session.commit()


def test_list_tasks_filter_by_status(client: TestClient, db_session: Session) -> None:
    seed_tasks(db_session)

    response = client.get("/api/tasks", params={"status": TaskStatus.TODO})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()["items"]] == ["Task 1"]


def test_list_tasks_filter_by_priority(client: TestClient, db_session: Session) -> None:
    seed_tasks(db_session)

    response = client.get("/api/tasks", params={"priority": TaskPriority.LOW})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()["items"]] == ["Task 2"]


def test_list_tasks_filter_by_status_and_priority(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)

    response = client.get(
        "/api/tasks", params={"status": TaskStatus.TODO, "priority": TaskPriority.LOW}
    )

    assert response.status_code == 200
    assert [task["title"] for task in response.json()["items"]] == []


def test_list_tasks_filter_by_wrong_status_return_422(client: TestClient) -> None:
    response = client.get("/api/tasks", params={"status": "wrong-status"})

    assert response.status_code == 422


def test_bookmark_task_returns_201(client: TestClient, db_session: Session) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    response = client.post(f"/api/tasks/{TASK_ID}/bookmark", headers=headers)

    assert response.status_code == 201
    assert response.json()["id"] == str(TASK_ID)


def test_bookmark_task_twice_returns_409(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    client.post(f"/api/tasks/{TASK_ID}/bookmark", headers=headers)
    response = client.post(f"/api/tasks/{TASK_ID}/bookmark", headers=headers)

    assert response.status_code == 409
    assert response.json()["detail"] == ERROR_TASK_BOOKMARKED


def test_bookmark_task_with_unknown_id_returns_404(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    response = client.post(f"/api/tasks/{UNKNOWN_ID}/bookmark", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == TASK_NOT_FOUND


def test_bookmark_task_without_token_returns_401(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)

    response = client.post(f"/api/tasks/{TASK_ID}/bookmark")

    assert response.status_code == 401


def test_bookmark_task_with_inactive_user_returns_403(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)

    headers = get_auth_headers(client)
    user = db_session.scalars(select(User).where(User.username == USER_NAME)).one()
    user.is_active = False
    db_session.commit()

    response = client.post(f"/api/tasks/{TASK_ID}/bookmark", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == USER_INACTIVE
