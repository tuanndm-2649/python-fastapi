from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from demo_fastapi.core.security import verify_password
from demo_fastapi.models import Project, Task, User
from demo_fastapi.tests.test_users import (
    EMAIL,
    PASSWORD,
    USER_NAME,
    register_user,
)


def test_register_login_and_create_task(
    client: TestClient,
    db_session: Session,
) -> None:
    response = register_user(client)

    assert response.status_code == 201

    user_data = response.json()
    assert user_data["email"] == EMAIL
    assert "password" not in user_data
    assert "hashed_password" not in user_data

    user = db_session.get(User, UUID(user_data["id"]))

    assert user is not None
    assert user.hashed_password != PASSWORD
    assert verify_password(PASSWORD, user.hashed_password)

    project = Project(name="Flow project", owner=user)
    db_session.add(project)
    db_session.commit()

    response = client.post(
        "/api/users/login",
        data={
            "username": USER_NAME,
            "password": PASSWORD,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.post(
        f"/api/projects/{project.id}/tasks",
        json={"title": "First task"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    task_data = response.json()
    assert task_data["title"] == "First task"
    assert task_data["project"]["id"] == str(project.id)

    task = db_session.get(Task, UUID(task_data["id"]))

    assert task is not None
    assert task.title == "First task"
    assert task.project_id == project.id
