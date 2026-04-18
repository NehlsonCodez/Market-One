from fastapi import APIRouter, HTTPException, Depends
from models import Product
from dependencies import get_current_user
from dependencies import get_db
from schemas import ProductCreate, ProductResponse
from sqlalchemy.orm import Session


def create_product(data : dict, db:Session):

    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product