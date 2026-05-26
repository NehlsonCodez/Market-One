from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException, status
from models import Category

async def category_create(data: dict, db:AsyncSession):

    try:
        result = await db.execute(select(Category).where(Category.name == data.name))
        category_exist = result.scalar_one_or_none()

        if category_exist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category already exist")

        new_category = Category(**data.model_dump())

        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        return new_category
    except Exception:
        await db.rollback()
        raise

async def get_all_categories(db:AsyncSession):
    
    result = await db.execute(select(Category))
    db_categories = result.scalars().all()
    if not db_categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
    
    return db_categories

async def get_category_by_id(id:int, db:AsyncSession):


    result = await db.execute(select(Category).where(Category.id == id))
    
    db_category = result.scalar_one_or_none()
    
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
    
    return db_category

async def update_category_by_id(id:int, category_data:dict, db:AsyncSession):
    
    try:
    
        result = await db.execute(select(Category).where(Category.id == id))

        db_category = result.scalar_one_or_none()

        if not db_category:
            raise HTTPException(status_code=401, detail="Category not found")
        
        db_category.name = category_data.name
        db_category.description = category_data.description

        await db.commit()
        return db_category
    
    except Exception:
        await db.rollback()
        raise


async def delete_category_by_id(id:int, db:AsyncSession):
    try:
        result = await db.execute(select(Category).where(Category.id == id))

        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
        
        await db.delete(category)
        await db.commit()

        return {"delete": "successful"}
    except Exception as e:
        await db.rollback()
        raise
    
    