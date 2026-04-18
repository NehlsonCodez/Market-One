from fastapi import APIRouter, HTTPException, Depends
from models import Product
from dependencies import get_current_user
from dependencies import get_db
from schemas import ProductCreate, ProductResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/create_product", response_model=ProductResponse)
async def create_product(product: ProductCreate, 
                         db: Session = Depends(get_db), 
                         current_user = Depends(get_current_user)):

    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin Only")
    
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/get_products")
async def get_products(db: Session = Depends(get_db), current_user =Depends(get_current_user)):
    products = db.query(Product).all()
    return products

@router.get("/get_product/{id:int}")
async def get_product(id:int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == id).first()
    return product