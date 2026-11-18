from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import USER_NOT_FOUND
from demo_fastapi.models import Project, User


def test_user_profile_returns_200_without_email(
    client: TestClient, db_session: Session
) -> None:
    user = User(
        name="User 1",
        username="user1",
        email="user1@example.com",
        hashed_password="test-only",
    )
    project = Project(name="Project 1", owner=user)
    db_session.add_all([user, project])
    db_session.commit()

    response = client.get("/api/users/user1/profile")

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "user1"
    assert [item["name"] for item in data["projects"]] == ["Project 1"]
    assert "email" not in data


def test_user_profile_unknown_username_returns_404(client: TestClient) -> None:
    response = client.get("/api/users/unknown/profile")

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND
