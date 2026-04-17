from fastapi import APIRouter, Depends, HTTPException
from schemas import UsersResponse, UserCreate, UserLogin, ProductResponse, ProductCreate, OrderCreate, OrderItemResponse, OrderResponse
from dependencies import get_db
from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from models import *
from core import create_access_token
from crud import create_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UsersResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db) ):
    # data = user.model_dump()
    # data.pop("confirm_password")

    # data["password"] = hash_password(data["password"])
    # new_user = User(**data)
    
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    return create_user(user,db)
    
    

@router.post("/login_user")
async def login_user(user: UserLogin, db: Session =Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user and verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Credential")
    
    token = create_access_token(data={"sub":db_user.id, "role":db_user.role})

    return {"access_token": token, "token_type": "Bearer"}

