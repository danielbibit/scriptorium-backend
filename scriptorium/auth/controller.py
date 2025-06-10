from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from scriptorium import database
from scriptorium.auth import schemas as auth_schemas
from scriptorium.auth import service as auth_service
from scriptorium.logging import get_logger

router = APIRouter()

log = get_logger()


@router.post("/auth")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(database.get_db),
) -> auth_schemas.AuthTokenResponse:
    log.debug("Login attempt for user: %s", form_data.username)
    return auth_service.authenticate_user(db, form_data.username, form_data.password)
