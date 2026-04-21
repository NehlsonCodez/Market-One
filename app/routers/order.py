from fastapi import APIRouter, Depends, HTTPException
from models import Order, OrderItem, Product
from utils import generate_unique_order_number
from schemas import OrderCreate, OrderResponse, OrderStatus
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/create_order", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    print("Start...")
    order_number = generate_unique_order_number(db)

    print(order_number)
    new_order = Order(user_id = current_user.id,
                      order_number = order_number,
                      total_amount = 0)
    print(new_order)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total = 0
    
    for item in order_data.items:
        print("start")
        product = db.query(Product).filter(Product.id == item.product_id).first()
        print("line1 confirm")
        if not product:
            raise HTTPException(status_code=404, detail="product not found!")
        
        price = product.price
        total_amount = price * item.quantity

        order_item = OrderItem(order_id = new_order.id,
                               product_id = product.id,
                               quantity = item.quantity,
                               price_at_purchased = price,
                               total_amount = total_amount)
        db.add(order_item)

        total += total_amount
        
    new_order.total_amount = total
    db.commit()
    db.refresh(new_order)

    return new_order

@router.get("/get_orders")
async def get_orders(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()

@router.get("/get_order/{id:int}")
async def get_order(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id==id).first()

    if not order:
        raise HTTPException(status_code=404, detail='order not found!')
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    return order

@router.put("/update_order/{order_id:int}") #Admin only
async def update_order_status(order_id:int, order_status:OrderStatus, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Admin only")
    
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.order_status = order_status
    db.commit()
    db.refresh(order)
    
    return {"Message":"Order updated successfully"}

@router.delete("/delete_order/{id}")
async def delete_order(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    db.query(Order).filter(Order.id==id).delete()
    db.commit()
    return {"Message": "Deleted Successfully"}