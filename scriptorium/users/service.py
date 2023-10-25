import logging

from sqlalchemy.orm import Session

from scriptorium.auth import service as auth_service
from scriptorium.users import models as users_models
from scriptorium.users import repository as users_repository
from scriptorium.users import schemas as users_schemas

log = logging.getLogger(__name__)


async def get_current_user(db: Session, token: str) -> users_models.User:
    user = await auth_service.get_auth_user(db, token)

    return user


def create_user(db: Session, user: users_schemas.UserCreate) -> users_models.User:
    hashed_password = auth_service.get_password_hash(user.password)

    user.password = hashed_password

    user_created = users_repository.create(db, user)

    return user_created


def get_all_users(db: Session):
    return users_repository.get_all_users(db)
