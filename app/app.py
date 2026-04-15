from fastapi import FastAPI, Depends, HTTPException
from schemas import UsersResponse, UserCreate, UserLogin
from dependencies import get_db
from database.database import Base, engine, Session
from utils import hash_password, verify_password
from  models import User

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"page": "Landing Page"}

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

@app.post("/login_user")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.username == user.username).first()

    if not (db_user and verify_password(user.password, db_user.password)):
        raise HTTPException(status_code=401, detail="Invalid Credetials")

    return {"Login": "Successful"}
