from fastapi.testclient import TestClient

from app.main import app
from app.security import get_current_user

app.dependency_overrides[get_current_user] = lambda: 1
client = TestClient(app)


def create_sample_order():
    payload = {
        "customer_name": "Joe Costa",
        "product": "Bermuda anti UV preta de corrida",
        "quantity": 2,
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_update_order_status_success():
    created_order = create_sample_order()
    order_id = created_order["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "processing"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == "processing"
    assert data["customer_name"] == "Joe Costa"
    assert data["product"] == "Bermuda anti UV preta de corrida"
    assert data["quantity"] == 2


def test_update_order_status_not_found():
    response = client.patch(
        "/orders/999999/status",
        json={"status": "processing"},
    )

    assert response.status_code == 404, response.text
    data = response.json()
    assert "detail" in data


def test_update_order_status_with_invalid_value():
    created_order = create_sample_order()
    order_id = created_order["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "invalid-status"},
    )

    assert response.status_code in (400, 422), response.text
