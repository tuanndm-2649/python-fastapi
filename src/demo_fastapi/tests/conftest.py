import os
from pathlib import Path

import pytest
from alembic.config import Config
from dotenv import dotenv_values
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from alembic import command

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def load_test_database_url() -> str:
    config = dotenv_values(PROJECT_ROOT / ".env.test")
    value = os.getenv("TEST_DATABASE_URL") or config.get("TEST_DATABASE_URL")

    if not value:
        raise pytest.UsageError("Missing TEST_DATABASE_URL")

    return value


TEST_DATABASE_URL = load_test_database_url()

url = make_url(TEST_DATABASE_URL)

if url.get_backend_name() != "postgresql" or not (
    url.database and url.database.endswith("_test")
):
    raise pytest.UsageError("Have to use _test database")

os.environ["DATABASE_URL"] = TEST_DATABASE_URL


@pytest.fixture(scope="session")
def test_engine():
    alembic_config = Config(str(PROJECT_ROOT / "alembic.ini"))
    command.upgrade(alembic_config, "head")

    engine = create_engine(TEST_DATABASE_URL)

    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(test_engine):
    with test_engine.connect() as connection:
        transaction = connection.begin()
        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session
        finally:
            session.close()
            transaction.rollback()


@pytest.fixture
def client(db_session):
    from demo_fastapi.database import get_db
    from demo_fastapi.main import app

    def override_get_db():
        yield db_session

    previous_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
