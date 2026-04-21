from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_db, get_current_user
from schemas import ProductCreate, ProductResponse, ProductUpdate
from sqlalchemy.orm import Session
from crud import product_create, update_product_by_id, get_product_by_id, get_all_products, delete_product_by_id

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/create_product", response_model=ProductResponse)
async def create_product(product: ProductCreate, 
                         db: Session = Depends(get_db), 
                         current_user = Depends(get_current_user)):

    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin Only")
    
    return product_create(product, db)


@router.get("/get_products")
async def get_products(db: Session = Depends(get_db), current_user =Depends(get_current_user)):
    return get_all_products(db)

@router.get("/get_product/{id:int}")
async def get_product(id:int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_product_by_id(id, db)

@router.put("/update_product/{id:int}")
async def update_product(id:int, product_data:ProductUpdate, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Admin Only")
    
    return update_product_by_id(id, product_data, db)
    
@router.delete("/delete_product/{id:int}")
async def delete_product(id:int, db:Session=Depends(get_db), current_user = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Admin Only")
    
    return delete_product_by_id(id, db)