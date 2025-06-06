from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from scriptorium.auth import repository as auth_repository
from scriptorium.auth import schemas as auth_schemas
from scriptorium.auth.exceptions import InvalidCredentials, InvalidToken
from scriptorium.config import config
from scriptorium.logging import get_logger
from scriptorium.users import repository as users_repository

log = get_logger()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(plain_password: str) -> str:
    password_bytes = bytes(plain_password, "utf-8")
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def create_access_token(token_data: auth_schemas.JWTToken) -> str:
    encoded_jwt = jwt.encode(dict(token_data), config.AUTH_SECRET_KEY, algorithm=config.AUTH_ALGORITHM)

    return encoded_jwt


def authenticate_user(db: Session, email: str, password: str) -> auth_schemas.AuthTokenResponse:
    log.debug("Authenticating user with email: %s", email)

    auth_data = auth_repository.get_auth_by_email(db, email)

    if not auth_data:
        log.error("Token not provided")

        raise InvalidCredentials()

    if not verify_password(password, auth_data.hashed_password):
        log.error("Invalid password for user %s", email)

        raise InvalidCredentials()

    jwt_token = auth_schemas.JWTToken(
        sub=str(auth_data.user_id),
        exp=datetime.now(timezone.utc) + timedelta(minutes=60),
        iat=datetime.now(timezone.utc),
    )

    log.debug("JWT Token creation data %s", jwt_token)

    token_string: str = create_access_token(jwt_token)

    log.debug("JWT Token created %s", token_string)

    return auth_schemas.AuthTokenResponse(access_token=token_string, token_type="bearer")


async def get_auth_user(db: Session, token: str):
    log.debug("token: %s", token)

    try:
        payload = jwt.decode(token, config.AUTH_SECRET_KEY, algorithms=[config.AUTH_ALGORITHM])

        log.debug(payload)

        user_id = payload.get("sub")

        if user_id is None:
            log.error("Invalid token")

            raise InvalidToken()

    except JWTError as e:
        log.error("JWT Error caught %s", e)

        raise InvalidToken()

    user = users_repository.get_by_id(db, user_id)

    if user is None:
        log.error("User dont exists")

        raise InvalidCredentials()

    return user
