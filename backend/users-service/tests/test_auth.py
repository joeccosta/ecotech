from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)


def create_test_user(name="Joe", email=None, password="Teste123"):
    unique_email = email or f"test-{uuid4().hex}@example.com"
    return client.post(
        "/users/",
        json={
            "name": name,
            "email": unique_email,
            "password": password,
        },
    )


def login_test_user(
    email: str,
    password: str = "Teste123",
):
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    return response


def test_login_returns_access_token():
    email = f"test-{uuid4().hex}@example.com"
    create_response = create_test_user(email=email)
    assert create_response.status_code in (200, 201), create_response.text

    login_response = login_test_user(email=email)
    assert login_response.status_code == 200, login_response.text

    data = login_response.json()
    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_secure_route_with_valid_token():
    create_response = create_test_user(
        email=f"secure-{uuid4().hex}@example.com",
        password="Teste123",
    )
    assert create_response.status_code in (200, 201), create_response.text

    email = create_response.json()["email"]
    login_response = login_test_user(
        email=email,
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
    assert "id" in data


def test_secure_route_without_token():
    response = client.get("/users/secure")
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Not authenticated"


def test_login_with_invalid_password():
    create_response = create_test_user(
        email=f"invalid-{uuid4().hex}@example.com",
        password="Teste123",
    )
    assert create_response.status_code in (200, 201), create_response.text

    login_response = login_test_user(
        email=create_response.json()["email"],
        password="SenhaErrada123",
    )

    assert login_response.status_code in (400, 401), login_response.text