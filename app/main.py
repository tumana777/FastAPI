from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.routers import categories, products, users, websockets
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging import log_request
from app.exceptions import ProductNotFound, ProductAlreadyExist
from app.handlers import (
    product_not_found_handler, product_already_exist_handler,
    global_exception_handler, validation_exception_handler
)

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
app.include_router(websockets.router)

# @app.exception_handler(ProductNotFound)
# async def product_not_found_handler(request: Request, exc: ProductNotFound):
#     return JSONResponse(
#         status_code=404,
#         content={"message": "Product not found"}
#     )

app.add_exception_handler(ProductNotFound, product_not_found_handler)
app.add_exception_handler(ProductAlreadyExist, product_already_exist_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)