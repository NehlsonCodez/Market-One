from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from .enums import UserRole

class UserBase(BaseModel):
    firstname : str
    lastname: str
    username : str
    email : EmailStr
    phone_number : str
    profile_picture : Optional[str] = None


class UsersResponse(UserBase):
    id : int

    model_config = ConfigDict(from_attributes = True)
    

class UserCreate(UserBase):
    role: UserRole = UserRole.CUSTOMER
    password : str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)

    @field_validator("confirm_password")
    def passwords_match(cls, value, info):
        password = info.data.get("password")
        if password and value != password:
            raise ValueError("passwords do not match!")
        return value
    
class UserLogin(BaseModel):
    username: str 
    password: str = Field(min_length=6)