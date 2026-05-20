from fastapi import HTTPException
from models import Cart, CartItem, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import Session, selectinload

async def add_item_to_cart(data: dict, db:AsyncSession, current_user:dict):
    
    try:
        result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
        
        cart = result.scalar_one_or_none()

        if data.quantity <= 0:
            raise HTTPException(status_code=400, detail="quantity must be greater than 0")
        
        if not cart:
            cart = Cart(user_id = current_user.id)

            db.add(cart)
            db.commit()
            db.refresh(cart)

        result = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id,
                                                        CartItem.product_id == data.product_id ))
        
        item_exist = result.scalar_one_or_none()

        if item_exist:
            item_exist.quantity += data.quantity

        else:
            product = db.execute(Product).filter(Product.id == data.product_id).first()

            if not product:
                raise HTTPException(status_code=404, detail="product not found")
            
            new_item = CartItem(cart_id = cart.id,
                                product_id = data.product_id,
                                quantity = data.quantity)
            
            db.add(new_item)

        await db.commit()
        
        return {"message": "added to cart"}
    
    except Exception:
        await db.rollback()
        raise

async def get_cart_items(db:AsyncSession, current_user:dict):

    cart = await db.execute(select(Cart).where(Cart.user_id == current_user.id)).options(selectinload(Cart.items))

    if not cart:
        raise HTTPException(status_code=400, detail="cart is empty")
    
    return cart

