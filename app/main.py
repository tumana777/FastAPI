from fastapi import FastAPI
from app.routers import categories, products

app = FastAPI(
    title="My First API",
    version="1.0.0",
    description="This is a simple API built with FastAPI."
)

app.include_router(categories.router)
app.include_router(products.router)