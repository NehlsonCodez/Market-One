from sqlalchemy.orm import Session
from models import Order
import random
from datetime import datetime, timezone

# function to generate order number using current datetime and random integers
def generate_order_number():
    random_part = random.randint(100000, 999999)
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"ORD-{date_part}-{random_part}"

# generate unique order number by cross-cheking if the generated one already exists 
# and generating another until it's not corresponding to any existing one in the database
def generate_unique_order_number(db: Session):
    while True:
        order_number = generate_order_number()

        existing_order_number = db.query(Order).filter(Order.order_number == order_number).first()

        if not existing_order_number:
            return order_number
        