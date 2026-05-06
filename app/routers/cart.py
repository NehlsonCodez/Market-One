from fastapi import APIRouter, HTTPException, Depends
from schemas import CartItemCreate, CartResponse, CartItemResponse, UpdateCartItem
from sqlalchemy.orm import Session, selectinload, joinedload
from models import Cart, CartItem, Product
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/item")
async def add_to_cart(item: CartItemCreate, db: Session=Depends(get_db), current_user = Depends(get_current_user)):

    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()


    if item.quantity <= 0: 
            raise HTTPException(status_code=400, detail="Quatity must be greater than 0" )
    
    
    if not cart:
        cart = Cart(user_id = current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    item_exists = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                                             CartItem.product_id == item.product_id).first()


    if item_exists:
        item_exists.quantity += item.quantity
    else:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found!")
        
        new_item = CartItem(cart_id = cart.id,
                            product_id=item.product_id,
                            quantity = item.quantity)
        db.add(new_item)
        
    
    db.commit()
    return {"message": "Added to cart"}
        

@router.get("/get_cart")
async def get_cart(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    cart = db.query(Cart).options(selectinload(Cart.items)).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code = 404, detail="Cart is empty!")
    
    return cart

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