from datetime import datetime

from pydantic import BaseModel


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str | None = None
    expires_in: int | None = None
    refresh_token: str | None = None
    scope: str | None = None


class JWTToken(BaseModel):
    sub: str
    exp: datetime
    iat: datetime | None = None
    jti: str = ""
    scope: str | None = None
    token_type: str | None = None
