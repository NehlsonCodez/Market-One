from fastapi import FastAPI, Depends, HTTPException
from schemas import UsersResponse, UserCreate, UserLogin, ProductResponse, ProductCreate, OrderCreate, OrderItemResponse, OrderResponse
from dependencies import get_db
from database.database import Base, engine
from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from  models import User, Product, Order, OrderItem
from dependencies import get_current_user
from core import create_access_token
from routers import auth_router, product_router, order_router, category_router
app = FastAPI(title="Market-One API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(category_router)

@app.get("/")
def index():
    return {"page": "Landing Page"}
