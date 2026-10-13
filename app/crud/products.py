from fastapi import Depends, HTTPException, status
from utils import save_upload
from models import Product, Category
from schemas import ProductCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json


async def product_create(product_data : dict, images, db:AsyncSession):

    # Parse JSON into existing Pydantic schema
    try:
        data_dict = json.loads(product_data)
        product_in = ProductCreate(**data_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON format in product_data")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid product data: {str(e)}")
    

    try:
        result = await db.execute(select(Category).where(Category.id == product_data.category_id))

        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(status_code=404, detail="category not found!")

        if product_data.price <= 0:
            raise HTTPException(status_code=401, detail="price must be greater than 0")

        if product_data.stock_quantity <= 0:
            raise HTTPException(status_code=401, detail="quantity must be greater than 0")
        
        #Save images using YOUR function
        image_urls: List[str] = []
        for image in images:
            try:
                image_url = save_upload(image, folder="products")   # ← Your exact function
                image_urls.append(image_url)
            except Exception as e:
                # Reraise with better status code if needed
                raise HTTPException(status_code=400, detail=str(e))
        

        new_product = Product(**product_data.model_dump())
        db.add(new_product)

        await db.commit()
        await db.refresh(new_product)
        
        return new_product
    except Exception:
        await db.rollback()
        raise

async def get_all_products(db:AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

async def get_product_by_id(id:int, db:AsyncSession):
    result = await db.execute(select(Product).where(Product.id == id))

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    
    return product

async def update_product_by_id(id:int, product_data: dict, db:AsyncSession):
    try:
        result = await db.execute(select(Product).where(Product.id == id))

        db_product = result.scalar_one_or_none()

        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
        
        db_product.name = product_data.name
        db_product.description = product_data.description
        db_product.price = product_data.price
        db_product.category_id = product_data.category_id
        db_product.stock_quantity = product_data.stock_quantity

        await db.commit()

        return {"message": "updated successfully"}
    
    except Exception:
        await db.rollback()
        raise



async def delete_product_by_id(id:int, db:AsyncSession):
    
    try:
        result = await db.execute(select(Product).where(Product.id  == id))
        
        print(result)
        
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "product not found!")
        
        await db.delete(product)
        await db.commit()
        
        return {"Message": "Product deleted successfully"}
        
    except Exception as e:
        await db.rollback()
        raise
    
    
