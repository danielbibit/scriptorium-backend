from typing import List

from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from scriptorium.auth import models as auth_models
from scriptorium.users import models as users_models
from scriptorium.users import schemas as users_schemas


def create(db: Session, user: users_schemas.UserCreate) -> users_models.User:
    db_user = users_models.UserORM(
        name=user.name,
        email=user.email,
        full_name=user.full_name,
    )

    db.add(db_user)
    db.flush()

    auth_user = auth_models.AuthORM(hashed_password=user.password, user_id=db_user.id)

    db.add(auth_user)

    db.commit()

    db.refresh(db_user)
    db.refresh(auth_user)

    return db_user.to_model()


def get_by_id(db: Session, user_id: str) -> users_models.User | None:
    user = db.get(users_models.UserORM, user_id)
    return users_models.User.model_validate(user)


def get_by_email(db: Session, email: str) -> users_models.User | None:
    user = db.query(users_models.UserORM).filter(users_models.UserORM.email == email).first()

    return users_models.User.model_validate(user)
    # return user.to_model()


def get_all_users(db: Session) -> List[users_models.User]:
    users = db.query(users_models.UserORM).all()

    userListValidator = TypeAdapter(List[users_models.User])

    return userListValidator.validate_python(users)
