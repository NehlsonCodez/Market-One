from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

class UserBase(BaseModel):
    firstname : str
    lastname: str
    username : str
    email : EmailStr
    phone : str


class UsersResponse(UserBase):
    id : int

    model_config = ConfigDict(from_attribute = True)
    

class UserCreate(UserBase):
    password : str = Field(min_length=6)
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, value, info):
        password = info.data.get("password")
        if password and value != password:
            raise ValueError("passwords do not match!")
        return value