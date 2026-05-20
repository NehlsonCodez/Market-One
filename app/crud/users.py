from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from core import create_access_token
from utils import hash_password, verify_password
from models import *
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

#Read User By ID
async def get_user_by_id(db : AsyncSession, user_id:int):
    
    result = await db.execute(select(User).where(User.id == user_id))
    
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    return user


#Read User By Username
async def get_user_by_username(db:AsyncSession, username:str):
    result = await db.execute(select(User).where(User.username == username))

    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    return user

#Create User
async def create_user(user_data:dict, db:AsyncSession):

    result = await db.execute(select(User).where(User.username == user_data.username))

    user_exist = result.scalar_one_or_none()

    if user_exist:
        raise HTTPException(status_code=400, detail="Username is already taken")

    data = user_data.model_dump()
    data.pop("confirm_password")

    data["password"] = hash_password(data["password"])

    new_user = User(**data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

#Login User
async def login_user(form_data:OAuth2PasswordRequestForm, db:AsyncSession):
    
    result = await db.execute(select(User).where(User.username == form_data.username))

    db_user = result.scalar_one_or_none()

    if not (db_user and verify_password(form_data.password, db_user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credential")
    
    token = create_access_token(data={"sub":str(db_user.id), "role":db_user.role})
    return {"access_token": token, "token_type" : "bearer"}

async def forgotten_password(email:str, db:AsyncSession):
    pass

async def reset_password(id:int, db:AsyncSession):
    pass