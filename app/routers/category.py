from fastapi import APIRouter, Depends, HTTPException
from schemas import CategoryResponse, CategoryCreate
from dependencies import get_db
from sqlalchemy.orm import Session
from crud import category_create
from dependencies import get_current_user


router = APIRouter(prefix="/category", tags=["category"])

@router.post("/create_category", response_model=CategoryResponse)
async def create_category(data:CategoryCreate, db: Session = Depends(get_db)
                          , current_user=Depends(get_current_user)):


    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Admin Only")
    
    return category_create(data, db)