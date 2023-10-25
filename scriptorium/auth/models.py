from uuid import UUID as UUIDType
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import UUID, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from scriptorium.database import Base
from scriptorium.users import models as users_models


class Auth(BaseModel):
    id: UUIDType
    hashed_password: str
    user_id: UUIDType
    user: users_models.User


class AuthORM(Base):
    __tablename__ = "auth"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, init=False, default=uuid4())

    hashed_password: Mapped[str] = mapped_column(String(64))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["users_models.UserORM"] = relationship("UserORM", init=False, single_parent=True)

    __table_args__ = (UniqueConstraint("user_id"),)


def create_fake_auth() -> Auth:
    return Auth(
        id=uuid4(),
        # Hashed password for "password"
        hashed_password="$2b$12$TKU/5SKzA8IyH.p830e.NeDnG.AHc5NJV9DE7NgwyShws8IJ8IDGO",
        user_id=uuid4(),
        user=users_models.create_fake_user(),
    )
