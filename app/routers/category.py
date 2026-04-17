from fastapi import APIRouter, Depends, HTTPException
from schemas import CategoryResponse, CategoryCreate
from dependencies import get_db
from sqlalchemy.orm import Session
from crud import category_create, get_category_by_id, get_all_categories
from dependencies import get_current_user


router = APIRouter(prefix="/category", tags=["category"])

@router.post("/create_category", response_model=CategoryResponse)
async def create_category(data:CategoryCreate, db: Session = Depends(get_db)
                          , current_user=Depends(get_current_user)):


    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Admin Only")
    
    return category_create(data, db)


@router.get("/get_categories")
async def get_categories(db:Session = Depends(get_db)):
    
    return get_all_categories(db)

@router.get("/get_category/{id:int}")
async def get_category(id:int, db: Session = Depends(get_db)):

    return get_category_by_id

@router.put("/update_category/{id:int}")
async def update_category(id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    pass

@router.delete("/delete_category/{id:int}")
async def delete_category(id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    pass