from fastapi import FastAPI, HTTPException
from models import Cart, Order, OrderItem
from utils import generate_unique_order_number
from sqlalchemy.orm import Session, selectinload

def order_create(db: Session, current_user:dict):

    cart = db.query(Cart).options(selectinload(Cart.items)).filter(Cart.id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="cart is empty")
    
    order_number = generate_unique_order_number(db)

    new_order = Order(user_id = current_user.id,
                        order_number = order_number,
                        total_amount = 0)
    
    db.add(new_order)
    db.flush()
    
    total = 0

    for item in cart.items:
        product = item.product

        if not product:
            raise HTTPException(status_code=404, detail="product not found!")
        
        price = product.price
        total_amount = price * item.quantity

        order_item = OrderItem(order_id = new_order.id,
                               product_id = product.id,
                               quantity = item.quantity,
                               price_at_purchased = price,
                               total_amount = total_amount )
        
        db.add(order_item)

        total += total_amount

    new_order.total_amount = total

    for item in cart.items:
        db.delete(item)

    db.commit()
    db.refresh(new_order)

    return new_order
    
def get_order_by_id(id:int, db:Session, current_user:dict):
    
    order = db.query(Order).filter(Order.id == id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not allowed")
    
    return order

def get_all_orders(db:Session, current_user:dict):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()

    return orders

def update_order_status_by_id(id:int, data:dict, db: Session):

    order = db.query(Order).filter(Order.id == id).first()

    order.order_status = data

    db.commit()
    db.refresh(order)

    return {"Message":"Order updated successfully"}

def delete_order_by_id(id, db:Session):

    order = db.query(Order).filter(Order.id == id).first()

    db.delete(order)
    db.commit()
    return {"message": "deleted successfully"}