from pydantic import BaseModel, ConfigDict

class CartItemBase(BaseModel):
    product_id : int
    quantity : int

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)