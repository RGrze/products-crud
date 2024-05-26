from app.api.v1.services.auth import get_user_from_api_key
from app.database.models.users import User


def test_get_user_from_api_key_on_non_existent_api_key(db_session):
    output = get_user_from_api_key(db_session, "non_existent_key")

    assert output is None


def test_get_user_from_api_key(db_session, add_api_key_and_user):
    expected_username = "test_user"

    output = get_user_from_api_key(db_session, "test_key")

    assert isinstance(output, User)
    assert expected_username == output.username
