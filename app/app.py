from fastapi import FastAPI
from schemas.users import UsersResponse, Users

app = FastAPI()

@app.get("/")
def index():
    return {"page": "Landing Page"}

@app.post("/create_user", response_model=UsersResponse)
def create_user(user: Users):
    data = user.dict()
    return data
