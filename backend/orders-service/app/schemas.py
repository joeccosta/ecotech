from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class OrderCreate(BaseModel):
    customer_name: str
    product: str
    quantity: int = Field(..., gt=0)  # A quantidade deve ser maior que 0


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    product: str
    quantity: int
    status: str
    created_at: datetime


class OrderStatusUpdate(BaseModel):
    status: str