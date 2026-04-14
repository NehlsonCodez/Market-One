from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_date = Column(DateTime, default = datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(12,2), nullable=False)
    order_status = Column(String(30))

    user = relationship('User', back_populates='orders')