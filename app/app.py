from fastapi import FastAPI, Depends, HTTPException
from schemas import UsersResponse, UserCreate, UserLogin, ProductResponse, ProductCreate, OrderCreate, OrderItemResponse, OrderResponse
from dependencies import get_db
from database.database import Base, engine
from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from  models import User, Product, Order, OrderItem
from dependencies import get_current_user
from core import create_access_token
from routers import auth_router, product_router, order_router
app = FastAPI(title="Market-One API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)

@app.get("/")
def index():
    return {"page": "Landing Page"}

#signup route
# @app.post("/create_user", response_model=UsersResponse)
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
#     data = user.model_dump()
#     data.pop("confirm_password")

#     data["password"] = hash_password(data["password"])
#     new_user = User(**data)
    
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


#login route
# @app.post("/login_user")
# async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    
#     #get tuple containing a row of a user table with the filtered username
#     db_user = db.query(User).filter(User.username == user.username).first()

#     #verify if the user exist and also confirm if the password is same as the stored password
#     if not (db_user and verify_password(user.password, db_user.password)):
#         raise HTTPException(status_code=401, detail="Invalid Credetials")

#     # later on add role and edit the data to {"role": db_user.role}
#     token = create_access_token(data={"sub" : db_user.id, "role": db_user.role})

#     return {"access_token": token, "token_type": "Bearer"}



# @app.post("/create_category")
# async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
#     pass

