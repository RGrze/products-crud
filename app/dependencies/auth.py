from typing import Annotated

from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.api.v1.services.auth import get_user_from_api_key
from app.database.db import get_db
from app.database.models.users import User

api_key_header = APIKeyHeader(name="X-API-Key")


def get_user(
    api_key: Annotated[str, Security(api_key_header)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    user = get_user_from_api_key(db, api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return user
