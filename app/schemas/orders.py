from pydantic import BaseModel, ConfigDict
from typing import List
from decimal import Decimal
from schemas import OrderItemBase, OrderItemResponse

class OrderCreate(BaseModel):
    user_id: int
    item : List[OrderItemBase]

class OrderResponse(BaseModel):
    id : int
    user_id: int
    total: Decimal
    items : List[OrderItemResponse]

    model_config = ConfigDict(from_attribute = True)