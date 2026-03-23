import pytest
from pydantic import ValidationError

from app.schemas import UserCreate, Token, UserResponse


def test_user_create_success():
    user = UserCreate(
        name="Joe Costa",
        email="joe@example.com",
        password="Teste123"
    )

    assert user.name == "Joe Costa"
    assert user.email == "joe@example.com"
    assert user.password == "Teste123"


def test_user_create_invalid_email():
    with pytest.raises(ValidationError) as exc:
        UserCreate(
            name="Joe Costa",
            email="email-invalido",
            password="Teste123",
        )

    errors = exc.value.errors()
    assert any(error["loc"] == ("email",) for error in errors)


def test_user_create_missing_name():
    with pytest.raises(ValidationError) as exc:
        UserCreate(
            email="joe@example.com",
            password="Teste123",
        )

    errors = exc.value.errors()
    assert any(error["loc"] == ("name",) for error in errors)


def test_user_create_short_password():
    with pytest.raises(ValidationError) as exc:
        UserCreate(
            name="Joe Costa",
            email="joe@example.com",
            password="12345",
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