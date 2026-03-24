from enum import Enum
from typing import Literal, get_args, get_origin

import pytest
from pydantic import ValidationError

from app.schemas import OrderCreate, OrderStatusUpdate


VALID_ORDER_PAYLOAD = {
    "customer_name": "Joe Costa",
    "product": "Camiseta ecológica",
    "quantity": 2,
    "price": 79.90,
}


def _error_fields(exc_info: pytest.ExceptionInfo[ValidationError]) -> list[str]:
    return [error["loc"][-1] for error in exc_info.value.errors()]


def _get_valid_status_value() -> str:
    status_field = OrderStatusUpdate.model_fields["status"]
    annotation = status_field.annotation

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return next(iter(annotation)).value

    if get_origin(annotation) is Literal:
        return get_args(annotation)[0]

    raise AssertionError("O campo 'status' não usa Enum nem Literal no schema atual.")


def test_order_create_accepts_valid_data():
    order = OrderCreate(**VALID_ORDER_PAYLOAD)

    assert order.customer_name == VALID_ORDER_PAYLOAD["customer_name"]
    assert order.product == VALID_ORDER_PAYLOAD["product"]
    assert order.quantity == VALID_ORDER_PAYLOAD["quantity"]
    assert order.price == VALID_ORDER_PAYLOAD["price"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("customer_name", ""),
        ("product", ""),
        ("quantity", 0),
        ("quantity", -1),
        ("price", 0),
        ("price", -10.5),
    ],
)
def test_order_create_rejects_invalid_business_fields(field, value):
    payload = VALID_ORDER_PAYLOAD.copy()
    payload[field] = value

    with pytest.raises(ValidationError) as exc_info:
        OrderCreate(**payload)

    assert field in _error_fields(exc_info)


@pytest.mark.parametrize(
    "missing_field",
    ["customer_name", "product", "quantity", "price"],
)
def test_order_create_requires_all_fields(missing_field):
    payload = VALID_ORDER_PAYLOAD.copy()
    payload.pop(missing_field)

    with pytest.raises(ValidationError) as exc_info:
        OrderCreate(**payload)

    assert missing_field in _error_fields(exc_info)


def test_order_status_update_accepts_valid_status():
    valid_status = _get_valid_status_value()

    status_update = OrderStatusUpdate(status=valid_status)

    assert status_update.status == valid_status


def test_order_status_update_rejects_invalid_status():
    with pytest.raises(ValidationError) as exc_info:
        OrderStatusUpdate(status="invalid_status_that_should_never_exist")

    assert "status" in _error_fields(exc_info)
