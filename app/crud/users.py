from sqlalchemy.orm import Session
from fastapi import HTTPException
from core import create_access_token
from utils import hash_password, verify_password
from models import *

#Read User By ID
def get_user_by_id(db : Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()


#Read User By Username
def get_user_by_username(db:Session, username:str):
    return db.query(User).filter(User.username == username)

#Create User
def create_user(user_data:dict, db:Session):
    data = user_data.model_dump()
    data.pop("confirm_password")

    data["password"] = hash_password(data["password"])

    new_user = User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Login User
def login_user(user_data: dict, db:Session):
    data = user_data.model_dump()
    db_user = db.query(User).filter(User.username == data.username).first()

    if not db_user and verify_password(data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Credential")
    
    token = create_access_token(data={"sub":db_user.id, "role":db_user.role})
    return {"Message" : "Login Successfull"}
