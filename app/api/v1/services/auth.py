from sqlalchemy.orm import Session

from app.database.models.users import ApiKey, User


def get_user_from_api_key(db: Session, api_key: str) -> User | None:
    ...
