from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from demo_fastapi.models import Tag


def test_list_tags_empty_returns_empty_list(client: TestClient) -> None:
    response = client.get("/api/tags")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tags_returns_all_tags(client: TestClient, db_session: Session) -> None:
    db_session.add_all([Tag(name="bug"), Tag(name="feature")])
    db_session.commit()

    response = client.get("/api/tags")

    assert response.status_code == 200
    assert len(response.json()) == 2
