from fastapi import APIRouter, Depends, HTTPException
from models import Order, OrderItem, Product, Cart, CartItem
from utils import generate_unique_order_number
from schemas import OrderResponse, OrderStatus
from sqlalchemy.orm import Session, selectinload
from dependencies import get_db, get_current_user
from crud import order_create, get_order_by_id, get_all_orders, update_order_status_by_id, delete_order_by_id

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/create_order", response_model=OrderResponse)
def create_order(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return order_create(db, current_user)

@router.get("/get_orders")
async def get_orders(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    return get_all_orders(db, current_user)

@router.get("/get_order/{id:int}")
async def get_order(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    return get_order_by_id(id, db, current_user)

@router.post("/order/{order_id}/pay")
async def initiate_payment(order_id:int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    
    if order.order_status != "pending":
        raise HTTPException(status_code=400, detail="Order has already been paid for or Cancelled")
    
    


@router.put("/update_order/{order_id:int}") #Admin only
async def update_order_status(order_id:int, order_status:OrderStatus, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Admin only")

    return update_order_status_by_id(order_id, order_status, db)

@router.delete("/delete_order/{id}")
async def delete_order(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    return delete_order_by_id(id, db)
