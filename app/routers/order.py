from fastapi import APIRouter, Depends, HTTPException
import requests
from models import Order, OrderItem, Product, Cart, CartItem, Payment
from utils import generate_unique_order_number
from schemas import OrderResponse, OrderStatus
from sqlalchemy.orm import Session, selectinload
from dependencies import get_db, get_current_user
from crud import order_create, get_order_by_id, get_all_orders, update_order_status_by_id, delete_order_by_id
from core import PAYSTACK_SECRET_KEY
import uuid

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
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    
    if order.order_status != "pending":
        raise HTTPException(status_code=400, detail="Order has already been paid for or Cancelled")
    
    #Call Paystack to initialize

    unique_reference = f"{order.order_number}--{uuid.uuid4().hex[:8]}"
    url = "https://api.paystack.co/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payment_data = {
        "email" : current_user.email,
        "amount" : int(order.total_amount * 100),
        "reference" : unique_reference,
        "metadata" : {
            "order_id" : order.id,
            "user_id" : current_user.id
        }
    }

    response = requests.post(url, json=payment_data, headers=headers)
    response_data = response.json()
    
    print(response_data)
    if not response_data.get("status"):

        raise HTTPException(status_code=400, detail="message: payment initializing failed")
    
    payment = Payment(user_id = current_user.id, order_id = order.id,
                      reference = unique_reference,
                      amount = order.total_amount,
                      status="pending")
    
    order.payment_reference = unique_reference

    db.add(payment)
    db.commit()

    return {
        "payment_url": response_data['data']['authorization_url'],
        "reference": response_data['data']['reference']
    }


@router.post("/verify/{reference}")
async def verify_payment(reference: str, db:Session=Depends(get_db), current_user=Depends(get_current_user) ):
    
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    headers = {
        "Authorization" : f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content_Type" : "application/json"
    }

    response = requests.get(url, headers=headers)

    response_data = response.json()

    if not response_data.get("status"):
        raise HTTPException(status_code=400, detail="verification failed")

    payment_data = response_data["data"]

    if payment_data.get("status") != "success":
        raise HTTPException(status_code=400, detail="payment not successful")
    
    order = db.query(Order).filter(Order.payment_reference == reference).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found!")
    
    order.payment_status = "paid"

    db.commit()

    return {"message": "payment verified successfully"}


@router.put("/update_order/{order_id:int}") #Admin only
async def update_order_status(order_id:int, order_status:OrderStatus, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Admin only")

    return update_order_status_by_id(order_id, order_status, db)

@router.delete("/delete_order/{id}")
async def delete_order(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    return delete_order_by_id(id, db)
