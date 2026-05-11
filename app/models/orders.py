from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_number = Column(String, unique=True, nullable=False)
    order_date = Column(DateTime, default = datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(12,2), nullable=False)
    order_status = Column(String(30), default="pending", nullable=False)

    #payments
    payment_status = Column(String(30), default="pending", nullable=False)
    payment_reference = Column(String, unique=True, nullable=True)
    payment_method = Column(String(30), default="Paystack")
    paid_at = Column(DateTime, nullable=True)

    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")