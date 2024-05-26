from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.users import ApiKey, User


def get_user_from_api_key(db: Session, key: str) -> User | None:
    """Receives user from database by api key.

    Args:
        db: Database session.
        key: Api key to search for.

    Returns:
        User object if key is found, None otherwise.

    """
    stmt = select(ApiKey).where(ApiKey.key == key)
    key = db.execute(stmt).scalar()
    if key is None:
        return None
    return key.user
