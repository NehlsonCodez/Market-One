from fastapi import FastAPI
from database.database import Base, engine
from routers import auth_router, product_router, order_router, category_router
app = FastAPI(title="Market-One API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(category_router)

@app.get("/")
def index():
    return {"page": "Landing Page"}
