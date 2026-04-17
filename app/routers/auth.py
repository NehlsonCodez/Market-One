from fastapi import APIRouter, Depends
from schemas import UsersResponse, UserCreate, UserLogin
from dependencies import get_db
from sqlalchemy.orm import Session
from crud import create_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UsersResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db) ):

    return create_user(user,db)
    
    
@router.post("/login")
async def login(user: UserLogin, db: Session =Depends(get_db)):
    
    return login_user(user,db)
