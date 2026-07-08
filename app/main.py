from fastapi import FastAPI
from app.routers import categories, products, users
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging import log_request

app = FastAPI(
    title="My First API",
    version="1.0.0",
    description="This is a simple API built with FastAPI."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_request)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)