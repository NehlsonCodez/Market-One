from fastapi import HTTPException
from models import Cart, CartItem, Product
from sqlalchemy.orm import Session, selectinload

def add_item_to_cart(data: dict, db:Session, current_user:dict):
    
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="quantity must be greater than 0")
    

    if not cart:
        cart = Cart(user_id = current_user.id)

        db.add(cart)
        db.commit()
        db.refresh(cart)

    item_exist = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                                           CartItem.product_id == data.product_id ).first()
    
    if item_exist:
        item_exist.quantity += data.quantity

    else:
        product = db.query(Product).filter(Product.id == data.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="product not found")
        
        new_item = CartItem(cart_id = cart.id,
                            product_id = data.product_id,
                            quantity = data.quantity)
        
        db.add(new_item)

    db.commit()
    return {"message": "added to cart"}

def get_cart_items(db:Session, current_user:dict):

    cart = db.query(Cart).options(selectinload(Cart.items)).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="cart is empty")
    
    return cart

