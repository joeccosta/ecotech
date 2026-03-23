from jose import jwt
from app.security import SECRET_KEY, ALGORITHM
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_auth_token(sub: str = "1") -> str:
    return jwt.encode({"sub": sub}, SECRET_KEY, algorithm=ALGORITHM)


def auth_headers(sub: str = "1") -> dict[str, str]:
    token = create_auth_token(sub=sub)
    return {"Authorization": f"Bearer {token}"}


def test_get_orders_returns_200():
    response = client.get("/orders")
    assert response.status_code == 200


def test_get_orders_returns_a_list():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_order_with_valid_payload():
    payload = {
        "customer_name": "Maria",
        "product": "Notebook",
        "quantity": 2
    }

    response = client.post("/orders", json=payload, headers=auth_headers())

    assert response.status_code in (200, 201)

    body = response.json()
    assert body["customer_name"] == "Maria"
    assert body["product"] == "Notebook"
    assert body["quantity"] == 2
    assert "id" in body
    assert "status" in body
    assert "created_at" in body


def test_create_order_with_invalid_payload():
    payload = {
        "customer_name": "Maria",
        "product": "Notebook"
    }

    response = client.post("/orders", json=payload, headers=auth_headers())

    assert response.status_code == 422
    
def test_create_order_missing_fields_returns_422():
    response = client.post("/orders", json={
        "customer_name": "Maria"
    }, headers=auth_headers())
    assert response.status_code == 422
    
def test_new_order_has_default_status_pending():
    """Regra de negócio: o status deve começar com pendente"""
    response = client.post("/orders", json={
        "customer_name": "João",
        "product": "Mouse",
        "quantity": 1
    }, headers=auth_headers())

    body = response.json()
    assert body["status"] == "pending"
    
def test_created_order_appears_in_list():
    """Deve persistir o dado"""
    create_response = client.post("/orders", json={
        "customer_name": "Ana",
        "product": "Viseira antiUV ecológica",
        "quantity": 1
    }, headers=auth_headers())
    
    assert create_response.status_code == 201

    response = client.get("/orders")
    body = response.json()

    assert any(order["customer_name"] == "Ana" for order in body)
    
def test_quantity_must_be_positive():
    response = client.post("/orders", json={
        "customer_name": "Pedro Russo",
        "product": "Camisa antiUV ecológica branca",
        "quantity": 0
    }, headers=auth_headers())

    assert response.status_code == 422
    
def test_quantity_must_be_greater_than_zero_for_negative_numbers():
    response = client.post("/orders", json={
        "customer_name": "Pedro Russo",
        "product": "Camisa antiUV ecológica branca",
        "quantity": -1
    }, headers=auth_headers())

    assert response.status_code == 422
    
def test_create_order_requires_authentication():
    response = client.post("/orders", json={
        "customer_name": "Maria",
        "product": "Notebook",
        "quantity": 2
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_create_order_with_invalid_token_returns_401():
    payload = {
        "customer_name": "Maria",
        "product": "Notebook",
        "quantity": 2
    }

    response = client.post(
        "/orders",
        json=payload,
        headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

