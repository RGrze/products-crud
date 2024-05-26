from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    password: str


class ApiKeyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    active: bool
    created_at: datetime


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    api_keys: list[ApiKeyOut] = []
