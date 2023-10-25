from sqlalchemy.orm import Session

from scriptorium.auth import models
from scriptorium.users import models as users_models


def get_auth_by_email(db: Session, email: str) -> models.Auth | None:
    query = (
        db.query(models.AuthORM).filter(models.AuthORM.user.has(users_models.UserORM.email == email)).first()
    )

    return models.Auth.model_validate(query) if query else None
