from fastapi.testclient import TestClient
from jose import jwt

from app.main import app
from app.security import ALGORITHM, SECRET_KEY

client = TestClient(app)


def create_auth_token(sub: str = "1") -> str:
    return jwt.encode({"sub": sub}, SECRET_KEY, algorithm=ALGORITHM)


def auth_headers(sub: str = "1") -> dict[str, str]:
    token = create_auth_token(sub=sub)
    return {"Authorization": f"Bearer {token}"}


def valid_order_payload(**overrides):
    payload = {
        "customer_name": "Maria",
        "product": "Short Feminino Ecotech",
        "quantity": 2,
        "price": 89.90,
    }
    payload.update(overrides)
    return payload


def test_get_orders_returns_200():
    response = client.get("/orders", headers=auth_headers())
    assert response.status_code == 200


def test_get_orders_returns_a_list():
    response = client.get("/orders", headers=auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_order_with_valid_payload():
    response = client.post(
        "/orders",
        json=valid_order_payload(),
        headers=auth_headers(),
    )

    assert response.status_code in (200, 201)

    body = response.json()
    assert body["customer_name"] == "Maria"
    assert body["product"] == "Short Feminino Ecotech"
    assert body["quantity"] == 2
    assert body["price"] == 89.90
    assert "id" in body
    assert "status" in body
    assert "created_at" in body


def test_create_order_with_invalid_payload():
    payload = {
        "customer_name": "Maria",
        "product": "Short Feminino Ecotech",
        "price": 89.90,
    }

    response = client.post("/orders", json=payload, headers=auth_headers())

    assert response.status_code == 422


def test_create_order_missing_fields_returns_422():
    response = client.post(
        "/orders",
        json={"customer_name": "Maria"},
        headers=auth_headers(),
    )
    assert response.status_code == 422


def test_new_order_has_default_status_pending():
    response = client.post(
        "/orders",
        json=valid_order_payload(
            customer_name="João",
            product="Boné",
            quantity=1,
            price=49.90,
        ),
        headers=auth_headers(),
    )

    assert response.status_code in (200, 201)
    body = response.json()
    assert body["status"] == "pending"


def test_created_order_appears_in_list():
    create_response = client.post(
        "/orders",
        json=valid_order_payload(
            customer_name="Ana",
            product="Viseira antiUV ecológica",
            quantity=1,
            price=59.90,
        ),
        headers=auth_headers(),
    )

    assert create_response.status_code in (200, 201)

    response = client.get("/orders", headers=auth_headers())
    body = response.json()

    assert any(
        order["customer_name"] == "Ana"
        and order["product"] == "Viseira antiUV ecológica"
        and order["quantity"] == 1
        and order["price"] == 59.90
        for order in body
    )


def test_quantity_must_be_positive():
    response = client.post(
        "/orders",
        json=valid_order_payload(
            customer_name="Pedro Russo",
            product="Camisa antiUV ecológica branca",
            quantity=0,
        ),
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_quantity_must_be_greater_than_zero_for_negative_numbers():
    response = client.post(
        "/orders",
        json=valid_order_payload(
            customer_name="Pedro Russo",
            product="Camisa antiUV ecológica branca",
            quantity=-1,
        ),
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_price_must_be_positive():
    response = client.post(
        "/orders",
        json=valid_order_payload(price=0),
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_price_must_be_greater_than_zero_for_negative_numbers():
    response = client.post(
        "/orders",
        json=valid_order_payload(price=-10.5),
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_customer_name_cannot_be_blank():
    response = client.post(
        "/orders",
        json=valid_order_payload(customer_name=""),
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_product_cannot_be_blank():
    response = client.post(
        "/orders",
        json=valid_order_payload(product=""),
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_create_order_requires_authentication():
    response = client.post("/orders", json=valid_order_payload())

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_list_orders_requires_authentication():
    response = client.get("/orders")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_order_requires_authentication():
    created = client.post(
        "/orders",
        json=valid_order_payload(
            customer_name="Carlos",
            product="Camiseta ecológica",
            quantity=1,
            price=69.90,
        ),
        headers=auth_headers(),
    )

    assert created.status_code in (200, 201)
    order_id = created.json()["id"]
    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_order_with_authentication_returns_200():
    created = client.post(
        "/orders",
        json=valid_order_payload(
            customer_name="Paula",
            product="Garrafa sustentável",
            quantity=1,
            price=39.90,
        ),
        headers=auth_headers(),
    )

    assert created.status_code in (200, 201)
    order_id = created.json()["id"]
    response = client.get(f"/orders/{order_id}", headers=auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == order_id
    assert body["customer_name"] == "Paula"
    assert body["price"] == 39.90


def test_update_status_requires_authentication():
    created = client.post(
        "/orders",
        json=valid_order_payload(
            customer_name="Bruno",
            product="Boné ecológico",
            quantity=1,
            price=29.90,
        ),
        headers=auth_headers(),
    )

    assert created.status_code in (200, 201)
    order_id = created.json()["id"]
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "processing"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
