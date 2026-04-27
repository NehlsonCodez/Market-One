from fastapi import APIRouter, HTTPException, Depends
from schemas import CartItemCreate, CartResponse, CartItemResponse
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

    item_exists = db.query(CartItem).filter(CartItem.cart_id == cart_exists.id,
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
        

@router.get("/get_cart", response_model=CartResponse)
async def get_cart(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code = 404, detail="Cart is empty!")
    
    return cart

@router.put("/update_cart_item/{id:int}")
async def update_cart_item(id:int, quantity:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == id,
        Cart.user_id == current_user.id
    ).first()
    
    cart_item.quantity = quantity
    
    db.commit()
    db.refresh(cart_item)
    return {"Message": "cart updated"}