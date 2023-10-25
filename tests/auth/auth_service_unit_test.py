import pytest
from pytest import MonkeyPatch


def test_verify_password():
    from scriptorium.auth import service

    password = "password"
    hashed_password = "$2b$12$TKU/5SKzA8IyH.p830e.NeDnG.AHc5NJV9DE7NgwyShws8IJ8IDGO"

    assert service.verify_password(password, hashed_password) is True

    wrong_password = "wrong"

    assert service.verify_password(wrong_password, hashed_password) is False


def test_get_password_hash(monkeypatch: MonkeyPatch):
    import bcrypt

    from scriptorium.auth import service

    def mock_salt():
        return b"$2b$12$ifnMdpYAw9zhHaNU3EnNz."

    monkeypatch.setattr(bcrypt, "gensalt", mock_salt)

    fake_hashed_password = service.get_password_hash("senha")

    assert fake_hashed_password == "$2b$12$ifnMdpYAw9zhHaNU3EnNz.HKa9mBgWR/38N6XUCfIEOWGJJiypKRC"


def test_create_access_token():
    import datetime

    from scriptorium.auth import schemas, service

    token_data = schemas.JWTToken(
        sub="1234567890",
        exp=datetime.datetime(2021, 4, 18, 18, 0),
        iat=datetime.datetime(2021, 4, 18, 17, 0),
    )

    token = service.create_access_token(token_data)

    assert (
        token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNjE4NzY4ODAwLCJpYXQiOjE2MTg3NjUyMDAsImp0aSI6IiIsInNjb3BlIjpudWxsLCJ0b2tlbl90eXBlIjpudWxsfQ.efNZMl_xwRdyjSCVcN1MRx2S1MTq4HAsmrFWPdU5CXg"
    )


def test_authenticate_user_raises_when_not_found(monkeypatch: MonkeyPatch):
    from sqlalchemy.orm import Session

    from scriptorium.auth import exceptions, service

    monkeypatch.setattr(
        "scriptorium.auth.repository.get_auth_by_email", lambda db, email: None  # type: ignore
    )

    with pytest.raises(exceptions.InvalidCredentials):
        service.authenticate_user(Session(), "test@test.com", "password")


def test_authenticate_user_raises_when_password_is_wrong(monkeypatch: MonkeyPatch):
    from sqlalchemy.orm import Session

    from scriptorium.auth import exceptions, models, service

    def mock_get_auth_by_email(db, email):  # type: ignore
        return models.create_fake_auth()

    monkeypatch.setattr("scriptorium.auth.repository.get_auth_by_email", mock_get_auth_by_email)  # type: ignore

    with pytest.raises(exceptions.InvalidCredentials):
        service.authenticate_user(Session(), "test@test.com", "password_wrong")


def test_authenticate_user_token_generation(monkeypatch: MonkeyPatch):
    from sqlalchemy.orm import Session

    from scriptorium.auth import models, service

    def mock_get_auth_by_email(db, email):  # type: ignore
        return models.create_fake_auth()

    monkeypatch.setattr("scriptorium.auth.repository.get_auth_by_email", mock_get_auth_by_email)  # type: ignore

    token = service.authenticate_user(Session(), "email@test.com", "password")
    print(token)
