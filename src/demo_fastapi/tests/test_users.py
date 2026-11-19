from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

from demo_fastapi.constants.auth import ALGORITHM
from demo_fastapi.constants.message import (
    EMAIL_ALREADY_EXISTS,
    INVALID_CREDENTIALS,
    INVALID_TOKEN,
    USER_NOT_FOUND,
    USERNAME_ALREADY_EXISTS,
)
from demo_fastapi.core.config import SECRET_KEY
from demo_fastapi.models import Project, User

PASSWORD = "password123"
USER_NAME = "user_test"
EMAIL = "user_test@example.com"


def register_user(
    client: TestClient,
    username: str = USER_NAME,
    email: str = "user_test@example.com",
    password: str = PASSWORD,
) -> Response:
    return client.post(
        "/api/users/register",
        json={
            "name": "User test",
            "email": email,
            "username": username,
            "password": password,
        },
    )


def get_auth_headers(client: TestClient) -> dict[str, str]:
    register_user(client)
    response = client.post(
        "/api/users/login", data={"username": USER_NAME, "password": PASSWORD}
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def make_auth_headers(payload: dict) -> dict[str, str]:
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"Authorization": f"Bearer {token}"}


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


def test_register_returns_201(client: TestClient) -> None:
    response = register_user(client)

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == EMAIL
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email_returns_409(client: TestClient) -> None:
    register_user(client)

    response = register_user(client, "user1")

    assert response.status_code == 409
    assert response.json()["detail"] == EMAIL_ALREADY_EXISTS


def test_register_duplicate_username_returns_409(client: TestClient) -> None:
    register_user(client)

    response = register_user(client, email="test@example.com")

    assert response.status_code == 409
    assert response.json()["detail"] == USERNAME_ALREADY_EXISTS


def test_register_password_with_accents_returns_422(client: TestClient) -> None:
    response = register_user(client, password="mậtkhẩu123")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "password"]


def test_register_username_with_space_returns_422(client: TestClient) -> None:
    response = register_user(client, username="user test")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "username"]


def test_register_username_with_slash_returns_422(client: TestClient) -> None:
    response = register_user(client, username="user/test")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "username"]


def test_register_email_is_lowercased(client: TestClient) -> None:
    response = register_user(client, email="User_Test@Example.com")

    assert response.status_code == 201
    assert response.json()["email"] == EMAIL


def test_login_success_return_access_token(client: TestClient) -> None:
    register_user(client, "login", "login@example.com")

    response = client.post(
        "/api/users/login", data={"username": "login", "password": PASSWORD}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_wrong_password_returns_401(client: TestClient) -> None:
    register_user(client)

    response = client.post(
        "/api/users/login", data={"username": USER_NAME, "password": "wrong-password"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == INVALID_CREDENTIALS


def test_login_password_with_accents_returns_401(client: TestClient) -> None:
    register_user(client)

    response = client.post(
        "/api/users/login", data={"username": USER_NAME, "password": "ệ" * 30}
    )

    assert response.status_code == 401


def test_get_me_returns_current_user(client: TestClient) -> None:
    headers = get_auth_headers(client)

    response = client.get("/api/users/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == EMAIL


def test_get_me_without_token_returns_401(client: TestClient) -> None:
    response = client.get("/api/users/me")

    assert response.status_code == 401


def test_get_me_invalid_token_returns_401(client: TestClient) -> None:
    response = client.get("/api/users/me", headers={"Authorization": "Bearer abc"})

    assert response.status_code == 401
    assert response.json()["detail"] == INVALID_TOKEN


def test_update_me_returns_updated_user(client: TestClient) -> None:
    headers = get_auth_headers(client)

    response = client.put("/api/users/me", json={"name": "New name"}, headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "New name"


def test_get_me_expired_token_returns_401(client: TestClient) -> None:
    headers = make_auth_headers(
        {
            "sub": str(uuid4()),
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        }
    )

    response = client.get("/api/users/me", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == INVALID_TOKEN


def test_get_me_with_wrong_payload_token_returns_401(client: TestClient) -> None:
    headers = make_auth_headers(
        {
            "sub": "abc",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        }
    )

    response = client.get("/api/users/me", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == INVALID_TOKEN
