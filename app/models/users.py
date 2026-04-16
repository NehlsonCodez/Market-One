from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email=Column(String(100), unique=True, nullable=False)
    role = Column(String(30), default="customer", nullable=False)
    password=Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable = True)
    isactive = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = relationship('Order', back_populates='user', cascade="all, delete-orphan")








