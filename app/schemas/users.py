from pydantic import BaseModel

class Users(BaseModel):
    id : int
    username : str
    email : str
    password : str
    phone : str


class UsersResponse(BaseModel):
    id : int
    username: str
    