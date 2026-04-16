from pydantic import BaseModel, ConfigDict
from typing import List

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price:int

class OrderItemResponse(OrderItemBase):
    id: int

    model_config = ConfigDict(from_attribute=True)
