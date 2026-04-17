from fastapi import APIRouter, Depends, HTTPException
from models import Order
from schemas import OrderCreate, OrderResponse
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/create_order", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    data = order.model_dump()
    new_order = Order(**data)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


@router.get("/get_orders")
async def get_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    orders = db.query(Order).all()
    return orders

@router.get("/get_order/{id:int}")
async def get_order(id:int, db:Session = Depends(get_db), current_user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == id).first()
    return order
