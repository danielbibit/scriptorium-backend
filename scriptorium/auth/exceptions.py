from scriptorium.exceptions import (
    HttpBadRequestException,
    HttpUnauthorizedException,
    ScriptoriumException,
)

# class ErrorCode:
# AUTHENTICATION_REQUIRED = "Authentication required."
# AUTHORIZATION_FAILED = "Authorization failed. User has no access."
# REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."


class AuthException(ScriptoriumException):
    pass


# class AuthRequired(AuthException, DetailedHTTPException):
#     DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


# class AuthorizationFailed(AuthException, DetailedHTTPException):
#     DETAIL = ErrorCode.AUTHORIZATION_FAILED
#     STATUS_CODE = status.HTTP_401_UNAUTHORIZED


class InvalidToken(AuthException, HttpBadRequestException):
    DETAIL = "Invalid token."


class InvalidCredentials(AuthException, HttpUnauthorizedException):
    DETAIL = "Invalid credentials."


class EmailTaken(AuthException, HttpBadRequestException):
    DETAIL = "Email is already taken."


class RefreshTokenNotValid(AuthException, HttpUnauthorizedException):
    DETAIL = "Refresh token is not valid."
