from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name: str
    description: str
    