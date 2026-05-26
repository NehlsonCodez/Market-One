from sqlalchemy.orm import Session
from models import Order
from sqlalchemy import select
import random
from datetime import datetime, timezone

# function to generate order number using current datetime and random integers
async def generate_order_number():
    random_part = random.randint(100000, 999999)
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"ORD-{date_part}-{random_part}"

# generate unique order number by cross-cheking if the generated one already exists 
# and generating another until it's not corresponding to any existing one in the database
async def generate_unique_order_number(db: Session):
    while True:
        order_number = await generate_order_number()

        result = await db.execute(select(Order).where(Order.order_number == order_number))

        existing_order_number = result.scalar_one_or_none()

        if not existing_order_number:
            return order_number
        