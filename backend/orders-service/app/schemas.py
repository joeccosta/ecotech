from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    product: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)  # A quantidade deve ser maior que 0
    
class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    product: str
    price: float
    quantity: int
    status: str
    created_at: datetime


class OrderStatusUpdate(BaseModel):
    status: OrderStatus