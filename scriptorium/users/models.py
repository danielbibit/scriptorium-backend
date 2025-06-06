from typing import Optional
from uuid import UUID as UUIDType
from uuid import uuid4

from faker import Faker
from pydantic import (
    BaseModel,
    ConfigDict,
)
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column

from scriptorium.database import Base


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUIDType
    name: str
    email: str
    full_name: str | None = None


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, init=False, default=uuid4())
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(40), unique=True)
    full_name: Mapped[Optional[str]] = mapped_column(default=None)

    def to_model(self) -> User:
        return User.model_validate(self)


def create_fake_user() -> User:
    fake = Faker()

    return User(
        id=fake.uuid4(),
        full_name=fake.name(),
        name=fake.name(),
        email=fake.email(),
    )
