from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.api.v1.models.users import UserOut, UserIn
from app.api.v1.services import users as users_srv
from app.database.db import get_db
from app.dependencies.auth import get_user
from app.database.models.users import User


router = APIRouter()


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(user: Annotated[User, Depends(get_user)]):
    return user


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
        db: Annotated[Session, Depends(get_db)],
        user: UserIn
):
    try:
        return users_srv.create_user(db, user)
    except ValueError:
        return Response(status_code=status.HTTP_409_CONFLICT)
