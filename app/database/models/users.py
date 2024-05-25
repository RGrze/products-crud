from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, func, ForeignKey

from app.database.db import Base


class ApiKey(Base):
    __tablename__ = "apikeys"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    key: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    active: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="api_keys")

    def __repr__(self):
        return f"<ApiKey key={self.key}>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    password_hash: Mapped[str]

    api_keys: Mapped[set["ApiKey"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User username={self.username}>"
