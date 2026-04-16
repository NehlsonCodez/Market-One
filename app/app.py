from fastapi import FastAPI, Depends, HTTPException
from schemas import UsersResponse, UserCreate, UserLogin, ProductResponse, ProductCreate, OrderCreate, OrderItemResponse, OrderResponse
from dependencies import get_db
from database.database import Base, engine
from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from  models import User, Product, Order, OrderItem
from dependencies import get_current_user
from core import create_access_token

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"page": "Landing Page"}

#signup route
@app.post("/create_user", response_model=UsersResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    data = user.model_dump()
    data.pop("confirm_password")

    data["password"] = hash_password(data["password"])
    new_user = User(**data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#login route
@app.post("/login_user")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    
    #get tuple containing a row of a user table with the filtered username
    db_user = db.query(User).filter(User.username == user.username).first()

    #verify if the user exist and also confirm if the password is same as the stored password
    if not (db_user and verify_password(user.password, db_user.password)):
        raise HTTPException(status_code=401, detail="Invalid Credetials")

    # later on add role and edit the data to {"role": db_user.role}
    token = create_access_token(data={"sub" : db_user.id, "role": db_user.role})

    return {"access_token": token, "token_type": "Bearer"}

@app.post("/create_product", response_model=ProductResponse)
async def create_product(product: ProductCreate, 
                         db: Session = Depends(get_db), 
                         current_user = Depends(get_current_user)):

    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin Only")
    
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)


@app.get("/get_products")
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/get_product/{id:int}")
async def get_product(id:int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    return product

# @app.post("/create_category")
# async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
#     pass

@app.post("/create_order", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    data = order.model_dump()
    new_order = Order(**data)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


@app.get("/get_orders")
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

@app.get("/get_order/{id:int}")
async def get_order(id:int, db:Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    return order

