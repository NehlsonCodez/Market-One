from fastapi import APIRouter, HTTPException, Depends
from schemas import CartItemCreate, UpdateCartItem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models import Cart, CartItem, Product
from dependencies import get_db, get_current_user
from crud import get_cart_items, add_item_to_cart

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/item")
async def add_to_cart(item: CartItemCreate, db: AsyncSession=Depends(get_db), current_user = Depends(get_current_user)):

    
    return await add_item_to_cart(item, db, current_user)
        

@router.get("/get_cart")
async def get_cart(db:AsyncSession=Depends(get_db), current_user = Depends(get_current_user)):
    
    return await get_cart_items(db, current_user)

@router.put("/update_cart_item/{id}")
async def update_cart_item(id:int, data: UpdateCartItem, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):

    try:

        result = await db.execute(select(CartItem).join(Cart).where(CartItem.id == id).where(Cart.user_id == current_user.id))

        cart_item = result.scalar_one_or_none()

        if not cart_item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        if data.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
        
        cart_item.quantity = data.quantity
        
        await db.commit()
        await db.refresh(cart_item)
        
        return {"message": "cart updated"}
    except Exception:
        await db.rollback()
        raise


@router.delete("/delete_cart")
async def delete_cart(db: AsyncSession = Depends(get_db),
                       current_user = Depends(get_current_user)):
    try:
        result = await db.execute(delete(Cart).wehre(Cart.user_id == current_user.id))

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="cart not found!")

        await db.commit()
        
        return {"message": "Deleted Cart"}
    except Exception:
        await db.rollback()
        raise