from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models import Category

def category_create(data: dict, db:Session):

    new_category = Category(**data.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category