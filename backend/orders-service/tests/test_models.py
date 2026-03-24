from datetime import datetime

from app.models import Order


def test_order_model_stores_expected_fields():
    order = Order(
        customer_name="Joe Costa",
        product="Camiseta ecológica",
        quantity=2,
        price=79.90,
        status="pending",
    )

    assert order.customer_name == "Joe Costa"
    assert order.product == "Camiseta ecológica"
    assert order.quantity == 2
    assert order.price == 79.90
    assert order.status == "pending"


def test_order_model_uses_default_created_at_and_status_when_not_informed():
    order = Order(
        customer_name="Maria",
        product="Jaqueta reciclada",
        quantity=1,
        price=149.50,
    )

    assert order.status == "pending"
    assert callable(Order.created_at.default.arg)
    assert Order.created_at.default.arg.__name__ == "utcnow"


def test_order_model_declares_non_nullable_required_fields():
    assert Order.__table__.columns["customer_name"].nullable is False
    assert Order.__table__.columns["product"].nullable is False
    assert Order.__table__.columns["quantity"].nullable is False
    assert Order.__table__.columns["price"].nullable is False


def test_order_model_declares_expected_column_types():
    assert Order.__table__.columns["id"].type.python_type is int
    assert Order.__table__.columns["customer_name"].type.python_type is str
    assert Order.__table__.columns["product"].type.python_type is str
    assert Order.__table__.columns["quantity"].type.python_type is int
    assert Order.__table__.columns["price"].type.python_type is float
    assert Order.__table__.columns["status"].type.python_type is str