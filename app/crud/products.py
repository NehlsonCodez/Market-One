from fastapi import Depends
from models import Product
from sqlalchemy.orm import Session


def product_create(product : dict, db:Session):

    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_all_products(db:Session):
    return db.query(Product).all()

def get_product_by_id(id:int, db:Session):
    return db.query(Product).filter(Product.id == id).first()

def update_product_by_id(id:int, product_data: dict, db:Session):
    db_product = db.query(Product).filter(Product.id == id).first()
    db_product.name = product_data.name
    db_product.description = product_data.description
    db_product.price = product_data.price
    db_product.category_id = product_data.category_id
    db_product.stock_quantity = product_data.stock_quantity
    db.commit()

    return db_product

def delete_product_by_id(id:int, db:Session):
    
    try:
        db.query(Product).filter(Product.id  == id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    
    return {"Message": "Product deleted successfully"}
