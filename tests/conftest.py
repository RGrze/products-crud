import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.database.db import Base, get_db, engine
from app.database.models.users import User, ApiKey
from app.database.models.products import Product, Label
from run import app


@pytest.fixture(scope="function", autouse=True)
def db_session() -> Session:
    Base.metadata.create_all(bind=engine)

    yield from get_db()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def add_api_key_and_user(db_session):
    user = User(
        username="test_user",
        password_hash="pwhash",
    )

    db_session.add(user)
    db_session.commit()

    api_key = ApiKey(key="test_key", active=True, user_id=user.id)

    db_session.add(api_key)
    db_session.commit()

    yield

    db_session.delete(api_key)
    db_session.delete(user)
    db_session.commit()


@pytest.fixture
def http_client(add_api_key_and_user):
    headers = {"X-API-Key": "test_key"}
    yield TestClient(app, headers=headers)
