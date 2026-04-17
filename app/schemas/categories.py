from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    name: str
    description: str = Field(None,max_length=500)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id : int

    model_config = ConfigDict(from_attribute=True)



    
    