from fastapi import APIRouter, HTTPException, Depends
from schemas import CartItemCreate
from sqlalchemy.orm import Session
from models import Cart, CartItem
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/item")
async def add_to_cart(item: CartItemCreate, db: Session=Depends(get_db), current_user = Depends(get_current_user)):

    cart_exists = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart_exists:
        cart = Cart(user_id = current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    item_exists = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                                             CartItem.product_id == item.product_id).first()

    if item_exists:
        item_exists.quantity += item.quantity
    else:
        new_item = CartItem(cart_id = cart.id,
                            product_id=item.product_id,
                            quantity = item.quantity)
        db. add(new_item)
    
    db.commit()
    return {"Message": "Added to cart"}
        

    