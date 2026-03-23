from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_test_user(
    name: str = "Joe Costa",
    email: str = "joe.auth@gmail.com",
    password: str = "Teste123",
):
    response = client.post(
        "/users/",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )
    return response


def login_test_user(
    email: str = "joe.auth@gmail.com",
    password: str = "Teste123",
):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    return response


def test_login_returns_access_token():
    create_response = create_test_user()
    assert create_response.status_code in (200, 201), create_response.text

    login_response = login_test_user()
    assert login_response.status_code == 200, login_response.text

    data = login_response.json()
    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_secure_route_with_valid_token():
    create_response = create_test_user(
        email="joe.secure@gmail.com",
        password="Teste123",
    )
    assert create_response.status_code in (200, 201), create_response.text

    login_response = login_test_user(
        email="joe.secure@gmail.com",
        password="Teste123",
    )
    assert login_response.status_code == 200, login_response.text

    token = login_response.json()["access_token"]

    secure_response = client.get(
        "/users/secure",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert secure_response.status_code == 200, secure_response.text
    data = secure_response.json()
    assert "user_id" in data


def test_secure_route_without_token():
    response = client.get("/users/secure")
    assert response.status_code == 401, response.text


def test_login_with_invalid_password():
    create_response = create_test_user(
        email="joe.invalid@gmail.com",
        password="Teste123",
    )
    assert create_response.status_code in (200, 201), create_response.text

    login_response = client.post(
        "/auth/login",
        json={
            "email": "joe.invalid@gmail.com",
            "password": "SenhaErrada123",
        },
    )

    assert login_response.status_code in (400, 401), login_response.text