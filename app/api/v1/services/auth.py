from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.users import ApiKey, User


def get_user_from_api_key(db: Session, api_key: str) -> User | None:
    stmt = select(ApiKey).where(ApiKey.key == api_key)
    api_key = db.execute(stmt).scalar()
    if api_key is None:
        return None
    return api_key.user
