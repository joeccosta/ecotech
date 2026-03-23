
import pytest
from pydantic import ValidationError

from app.schemas import UserCreate, UserLogin, Token, UserResponse


def test_user_create_success():
    user = UserCreate(
        name="Joe Costa",
        email="joe@example.com",
    )

    assert user.name == "Joe Costa"
    assert user.email == "joe@example.com"


def test_user_create_invalid_email():
    with pytest.raises(ValidationError) as exc:
        UserCreate(
            name="Joe Costa",
            email="email-invalido",
        )

    errors = exc.value.errors()
    assert any(error["loc"] == ("email",) for error in errors)


def test_user_create_missing_name():
    with pytest.raises(ValidationError) as exc:
        UserCreate(
            email="joe@example.com",
        )

    errors = exc.value.errors()
    assert any(error["loc"] == ("name",) for error in errors)


def test_user_login_success():
    login = UserLogin(
        email="joe@example.com",
        password="123456",
    )

    assert login.email == "joe@example.com"
    assert login.password == "123456"


def test_user_login_invalid_email():
    with pytest.raises(ValidationError) as exc:
        UserLogin(
            email="invalido",
            password="123456",
        )

    errors = exc.value.errors()
    assert any(error["loc"] == ("email",) for error in errors)


def test_user_login_missing_password():
    with pytest.raises(ValidationError) as exc:
        UserLogin(
            email="joe@example.com",
        )

    errors = exc.value.errors()
    assert any(error["loc"] == ("password",) for error in errors)


def test_token_success():
    token = Token(access_token="abc123")

    assert token.access_token == "abc123"
    assert token.token_type == "bearer"


def test_token_custom_type():
    token = Token(access_token="abc123", token_type="custom")

    assert token.access_token == "abc123"
    assert token.token_type == "custom"


def test_user_response_success():
    user = UserResponse(
        id=1,
        name="Joe Costa",
        email="joe@example.com",
    )

    assert user.id == 1
    assert user.name == "Joe Costa"
    assert user.email == "joe@example.com"


def test_user_response_invalid_email():
    with pytest.raises(ValidationError) as exc:
        UserResponse(
            id=1,
            name="Joe Costa",
            email="email-invalido",
        )

    errors = exc.value.errors()
    assert any(error["loc"] == ("email",) for error in errors)