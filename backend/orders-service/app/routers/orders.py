from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Order
from ..schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from ..security import get_current_user

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
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    status: str | None = None,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user),
):
    query = db.query(Order)

    if status:
        query = query.filter(Order.status == status)

    return query.all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

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
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = payload.status.value
    db.commit()
    db.refresh(order)

    return order