from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.status is None:
            self.status = "pending"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    