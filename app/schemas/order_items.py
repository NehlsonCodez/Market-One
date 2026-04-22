from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(OrderItemBase):
    id : int
    product_id : int
    quantity : int
    price_at_purchased :Decimal
    total_amount: Decimal

    model_config = ConfigDict(from_attributes=True)
