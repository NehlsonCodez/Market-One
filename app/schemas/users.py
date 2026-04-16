from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    firstname : str
    lastname: str
    username : str
    email : EmailStr
    phone_number : str


class UsersResponse(UserBase):
    id : int

    model_config = ConfigDict(from_attribute = True)
    

class UserCreate(UserBase):
    role: Optional[str]
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