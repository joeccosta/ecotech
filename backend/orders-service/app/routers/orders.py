import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Order
from ..schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from ..security import get_current_user

logger = logging.getLogger("orders-service")

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user),
):
    order = Order(
        customer_name=payload.customer_name,
        product=payload.product,
        quantity=payload.quantity,
        price=payload.price,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    logger.info(
        "order_created",
        extra={
            "event": "order_created",
            "order_id": order.id,
            "customer_name": order.customer_name,
            "status": order.status,
            "price": order.price,
        },
    )
    return order


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    status: str | None = None,
    order_id: int | None = None,
    customer_name: str | None = None,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user),
):
    query = db.query(Order)

    if order_id is not None:
        query = query.filter(Order.id == order_id)

    if customer_name:
        query = query.filter(Order.customer_name.ilike(f"%{customer_name}%"))

    if status:
        query = query.filter(Order.status == status)

    orders = query.all()

    logger.info(
        "orders_listed",
        extra={
            "event": "orders_listed",
            "status_filter": status,
            "order_id_filter": order_id,
            "customer_name_filter": customer_name,
            "result_count": len(orders),
        },
    )

    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        logger.warning(
            "order_not_found",
            extra={
                "event": "order_not_found",
                "order_id": order_id,
            },
        )
        raise HTTPException(status_code=404, detail="Order not found")

    logger.info(
        "order_retrieved",
        extra={
            "event": "order_retrieved",
            "order_id": order.id,
            "status": order.status,
        },
    )

    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        logger.warning(
            "order_not_found",
            extra={
                "event": "order_not_found",
                "order_id": order_id,
            },
        )
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = order.status
    order.status = payload.status.value
    db.commit()
    db.refresh(order)

    logger.info(
        "order_status_updated",
        extra={
            "event": "order_status_updated",
            "order_id": order.id,
            "old_status": old_status,
            "new_status": order.status,
        },
    )
    return order