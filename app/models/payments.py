from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False, index=True)
    
    reference = Column(String(100), unique=True, nullable=False, index=True)   # Unique & indexed
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(20), default="NGN", nullable=False)
    status = Column(String(50), default="pending", nullable=False)  # pending, success, failed, refunded
    payment_method = Column(String(50), nullable=True)
    
    # Paystack specific fields
    transaction_id = Column(String(100), nullable=True)        # Paystack's internal ID
    gateway_response = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="payments")

    order = relationship("Order", back_populates="payments")