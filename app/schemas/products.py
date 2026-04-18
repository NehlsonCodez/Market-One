from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class ProductBase(BaseModel):
    name : str
    description : str
    price : Decimal
    category_id : int
    stock_quantity: int


class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    int

    model_config = ConfigDict(from_attribute=True)

