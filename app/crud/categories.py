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

def update_category():
    pass

def delete_category():
    pass