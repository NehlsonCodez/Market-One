from fastapi import APIRouter, HTTPException, Depends
from schemas import CartItemCreate, CartResponse, CartItemResponse, UpdateCartItem
from sqlalchemy.orm import Session, selectinload, joinedload
from models import Cart, CartItem, Product
from dependencies import get_db, get_current_user
from crud import get_cart_items, add_item_to_cart

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/item")
async def add_to_cart(item: CartItemCreate, db: Session=Depends(get_db), current_user = Depends(get_current_user)):

    
    return add_item_to_cart(item, db, current_user)
        

@router.get("/get_cart")
async def get_cart(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    
    return get_cart_items(db, current_user)

@router.put("/update_cart_item/{id}")
async def update_cart_item(id:int, data: UpdateCartItem, db:Session=Depends(get_db), current_user=Depends(get_current_user)):


    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == id,
        Cart.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    cart_item.quantity = data.quantity
    
    db.commit()
    db.refresh(cart_item)
    return {"message": "cart updated"}


@router.delete("/delete_cart")
async def delete_cart(db: Session = Depends(get_db),
                       current_user = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code=404, detail= "Cart not found!")
    
    db.delete(cart)
    db.commit()
    return {"message": "Deleted Cart"}