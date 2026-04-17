from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models import Category

def category_create(data: dict, db:Session):

    new_category = Category(**data.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

def get_all_categories(db:Session):
    
    return db.query(Category).all()

def get_category_by_id(id:int, db:Session):

    return db.query(Category).filter(Category.id == id).first()

def update_category_by_id(id:int, category_data:dict, db:Session):
    db_category = db.query(Category).filter(Category.id == id).first()

    if not db_category:
        raise HTTPException(status_code=401, detail="Category not found")
    
    db_category.name = category_data.name
    db_category.description = category_data.description

    db.commit()
    return db_category


def delete_category_by_id(id:int, db:Session):
    try:
        db.query(Category).filter(Category.id == id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    
    return {"delete": "successful"}