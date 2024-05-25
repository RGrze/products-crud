import pytest

from app.api.v1.services.auth import get_user_from_api_key
from app.database.models.users import ApiKey, User


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


def test_get_user_from_api_key_on_non_existent_api_key(db_session):
    output = get_user_from_api_key(db_session, "non_existent_key")

    assert output is None


def test_get_user_from_api_key(db_session, add_api_key_and_user):
    expected_username = "test_user"

    output = get_user_from_api_key(db_session, "test_key")

    assert isinstance(output, User)
    assert expected_username == output.username
