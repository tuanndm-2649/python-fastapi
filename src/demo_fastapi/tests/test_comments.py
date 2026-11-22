from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import (
    COMMENT_NOT_FOUND,
    NOT_COMMENT_OWNER,
    TASK_NOT_FOUND,
)
from demo_fastapi.models import Comment, Task, User
from demo_fastapi.tests.test_project import UNKNOWN_ID, sign_token_for_owner
from demo_fastapi.tests.test_task import TASK_ID, seed_tasks
from demo_fastapi.tests.test_users import (
    USER_NAME,
    get_auth_headers,
    make_admin,
    seed_user,
    sign_token_for_user,
)

COMMENT_ID = UUID(int=20)


def seed_comment(db_session: Session, author: User, task_id: UUID = TASK_ID) -> Comment:
    comment = Comment(
        id=COMMENT_ID, content="Comment 1", task_id=task_id, author=author
    )
    db_session.add(comment)
    db_session.commit()

    return comment


def test_create_comment_returns_201(client: TestClient, db_session: Session) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    response = client.post(
        f"/api/tasks/{TASK_ID}/comments", json={"content": "Hello"}, headers=headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Hello"
    assert data["task_id"] == str(TASK_ID)
    assert data["author"]["username"] == USER_NAME


def test_create_comment_with_empty_content_returns_422(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    response = client.post(
        f"/api/tasks/{TASK_ID}/comments", json={"content": ""}, headers=headers
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "content"]


def test_create_comment_with_only_spaces_returns_422(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    response = client.post(
        f"/api/tasks/{TASK_ID}/comments", json={"content": "   "}, headers=headers
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "content"]


def test_create_comment_unknown_task_returns_404(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    response = client.post(
        f"/api/tasks/{UNKNOWN_ID}/comments", json={"content": "Hello"}, headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == TASK_NOT_FOUND


def test_create_comment_without_token_returns_401(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)

    response = client.post(f"/api/tasks/{TASK_ID}/comments", json={"content": "Hello"})

    assert response.status_code == 401


def test_delete_comment_by_author_returns_204(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)

    response = client.delete(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        headers=sign_token_for_user(author),
    )

    assert response.status_code == 204
    assert db_session.get(Comment, COMMENT_ID) is None


def test_delete_comment_by_admin_returns_204(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)
    headers = get_auth_headers(client)
    make_admin(db_session, USER_NAME)

    response = client.delete(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}", headers=headers
    )

    assert response.status_code == 204
    assert db_session.get(Comment, COMMENT_ID) is None


def test_delete_comment_by_project_owner_returns_204(
    client: TestClient, db_session: Session
) -> None:
    project = seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)

    response = client.delete(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        headers=sign_token_for_owner(project),
    )

    assert response.status_code == 204
    assert db_session.get(Comment, COMMENT_ID) is None


def test_delete_comment_by_other_user_returns_403(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)
    headers = get_auth_headers(client)

    response = client.delete(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}", headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == NOT_COMMENT_OWNER


def test_delete_unknown_comment_returns_404(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    headers = get_auth_headers(client)

    response = client.delete(
        f"/api/tasks/{TASK_ID}/comments/{UNKNOWN_ID}", headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == COMMENT_NOT_FOUND


def test_delete_comment_of_other_task_returns_404(
    client: TestClient, db_session: Session
) -> None:
    project = seed_tasks(db_session)
    other_task = Task(title="Other task", project=project)
    db_session.add(other_task)
    db_session.commit()
    author = seed_user(db_session, "author")
    seed_comment(db_session, author, task_id=other_task.id)

    response = client.delete(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        headers=sign_token_for_user(author),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == COMMENT_NOT_FOUND


def test_delete_comment_without_token_returns_401(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)

    response = client.delete(f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}")

    assert response.status_code == 401
    assert db_session.get(Comment, COMMENT_ID) is not None


def test_update_comment_by_author_returns_200(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)

    response = client.patch(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        json={"content": "Updated"},
        headers=sign_token_for_user(author),
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Updated"


def test_update_comment_by_admin_returns_200(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)
    headers = get_auth_headers(client)
    make_admin(db_session, USER_NAME)

    response = client.patch(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        json={"content": "Updated"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Updated"


def test_update_comment_by_project_owner_returns_200(
    client: TestClient, db_session: Session
) -> None:
    project = seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)

    response = client.patch(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        json={"content": "Updated"},
        headers=sign_token_for_owner(project),
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Updated"


def test_update_comment_by_other_user_returns_403(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)
    headers = get_auth_headers(client)

    response = client.patch(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        json={"content": "Updated"},
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == NOT_COMMENT_OWNER


def test_update_comment_with_empty_content_returns_422(
    client: TestClient, db_session: Session
) -> None:
    seed_tasks(db_session)
    author = seed_user(db_session, "author")
    seed_comment(db_session, author)

    response = client.patch(
        f"/api/tasks/{TASK_ID}/comments/{COMMENT_ID}",
        json={"content": ""},
        headers=sign_token_for_user(author),
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "content"]
