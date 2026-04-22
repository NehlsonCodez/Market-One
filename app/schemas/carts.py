from pydantic import BaseModel, ConfigDict
from typing import List
from schemas import CartItemResponse

class CartResponse(BaseModel):
    id: int
    user_id : int
    items : List[CartItemResponse]

    model_config = ConfigDict(from_attributes=True)