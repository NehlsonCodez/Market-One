from pydantic import BaseModel, ConfigDict
from typing import List
from decimal import Decimal
from schemas import OrderItemBase, OrderItemResponse

class OrderCreate(BaseModel):
    items : List[OrderItemBase]

class OrderResponse(BaseModel):
    id : int
    order_number: str
    user_id: int
    total_amount: Decimal
    items : List[OrderItemResponse]

    model_config = ConfigDict(from_attributes = True)