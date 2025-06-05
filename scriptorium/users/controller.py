from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from scriptorium import database
from scriptorium.users import models as users_models
from scriptorium.users import schemas as users_schemas
from scriptorium.users import service as users_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

router = APIRouter()


@router.get("/users")
def read_users(
    db: Annotated[Session, Depends(database.get_db)],
) -> List[users_models.User]:
    return users_service.get_all_users(db)


@router.post("/users")
def create_user(db: Annotated[Session, Depends(database.get_db)], user: users_schemas.UserCreate) -> users_models.User:
    return users_service.create_user(db, user)


@router.get("/users/me")
async def read_users_me(
    db: Annotated[Session, Depends(database.get_db)], token: Annotated[str, Depends(oauth2_scheme)]
) -> users_models.User:
    return await users_service.get_current_user(db, token)
