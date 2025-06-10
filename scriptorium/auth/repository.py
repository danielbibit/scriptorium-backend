from sqlalchemy.orm import Session

from scriptorium.auth import models
from scriptorium.logging import get_logger
from scriptorium.users import models as users_models

log = get_logger()


def get_auth_by_email(db: Session, email: str) -> models.Auth | None:
    query = (
        db.query(models.AuthORM).filter(models.AuthORM.user.has(users_models.UserORM.email == email)).first()
    )
    return query.to_model() if query else None
