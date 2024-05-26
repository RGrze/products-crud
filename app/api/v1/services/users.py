import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.models.users import UserIn
import app.database.models.users as users_orm


def get_user(db: Session, username: str) -> users_orm.User:
    """Get single user by username.

    Args:
        db: SQLAlchemy session
        username: Username

    Returns:
        User entity.
    """
    stmt = select(users_orm.User).where(users_orm.User.username == username)
    user = db.execute(stmt).scalar()
    if not user:
        raise ValueError("User not found")
    return user


def create_user(db: Session, user_in: UserIn) -> users_orm.User:
    """Create a new user.

    When user is created, a new API key is generated.

    Args:
        db: SQLAlchemy session
        user_in: User schema

    Returns:
        Created user entity.
    """
    try:
        get_user(db, user_in.username)
    except ValueError:
        pw_hash = user_in.password + "not_really_hashed"
        user = users_orm.User(username=user_in.username, password_hash=pw_hash)

        apikey = users_orm.ApiKey(key=secrets.token_urlsafe(4), active=True)

        db.add_all([apikey, user])
        db.flush()

        user.api_keys.add(apikey)

        db.commit()

        return user
