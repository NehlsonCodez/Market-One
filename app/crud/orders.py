from fastapi import FastAPI, HTTPException, status
from models import Cart, Order, OrderItem, CartItem
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from utils import generate_unique_order_number
from sqlalchemy.orm import selectinload

async def order_create(db: AsyncSession, current_user:dict):

    try:
        result = await db.execute(select(Cart).where(Cart.user_id == current_user.id).options(selectinload(Cart.items).selectinload(CartItem.product)))
        
        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(status_code=400, detail="cart is empty")
        
        order_number = await generate_unique_order_number(db)

        new_order = Order(user_id = current_user.id,
                            order_number = order_number,
                            total_amount = 0)
        
        db.add(new_order)
        await db.flush()
        
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
            await db.delete(item)


        await db.commit()
        await db.refresh(new_order)

        result = await db.execute(select(Order).where(Order.id == new_order.id)
                                  .options(selectinload(Order.items).selectinload(OrderItem.product)))
        
        order = result.scalar_one_or_none()
        
        return order
    
    except Exception:
        await db.rollback()
        raise


async def get_order_by_id(id:int, db:AsyncSession, current_user:dict):
    
    result = await db.execute(select(Order).where(Order.id == id))

    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not allowed")
    
    return order

async def get_all_orders(db:AsyncSession, current_user:dict):
    
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))

    orders = result.scalars().all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")


    return orders

async def update_order_status_by_id(id:int, data:dict, db: AsyncSession):

    try:
        result = await db.execute(select(Order).where(Order.id == id))

        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

        order.order_status = data

        await db.commit()
        await db.refresh(order)

        return {"Message":"Order updated successfully"}
    
    except Exception:
        await db.rollback()
        raise

async def delete_order_by_id(id:int, db:AsyncSession):

    try:
        result = await db.execute(select(Order).where(Order.id == id))

        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
        
        await db.delete(order)
        await db.commit()
        
        return {"message": "deleted successfully"}
    
    except Exception:
        await db.rollback()
        raise