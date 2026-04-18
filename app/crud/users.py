from sqlalchemy.orm import Session
from fastapi import HTTPException
from core import create_access_token
from utils import hash_password, verify_password
from models import *
from fastapi.security import OAuth2PasswordRequestForm

#Read User By ID
def get_user_by_id(db : Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()


#Read User By Username
def get_user_by_username(db:Session, username:str):
    return db.query(User).filter(User.username == username).first()

#Create User
def create_user(user_data:dict, db:Session):

    user_exist = db.query(User).filter(User.username == user_data.username).first()

    if user_exist:
        raise HTTPException(status_code=400, detail="Username is already taken")

    data = user_data.model_dump()
    data.pop("confirm_password")

    data["password"] = hash_password(data["password"])

    new_user = User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Login User
def login_user(form_data:OAuth2PasswordRequestForm, db:Session):
    
    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not (db_user and verify_password(form_data.password, db_user.password)):
        raise HTTPException(status_code=401, detail="Invalid Credential")
    
    token = create_access_token(data={"sub":str(db_user.id), "role":db_user.role})
    return {"access_token": token, "token_type" : "bearer"}
