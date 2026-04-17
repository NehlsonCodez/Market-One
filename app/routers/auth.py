from fastapi import APIRouter, Depends
from schemas import UsersResponse, UserCreate, UserLogin
from dependencies import get_db
from sqlalchemy.orm import Session
from crud import create_user, login_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UsersResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db) ):

    return create_user(user,db)
    
    
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm=Depends() , db: Session =Depends(get_db)):
    
    return login_user(form_data, db)
