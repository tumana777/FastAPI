from app.exceptions import ProductNotFound, ProductAlreadyExist
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def product_not_found_handler(request: Request, exc: ProductNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": "Product not found"}
    )

async def product_already_exist_handler(request: Request, exc: ProductAlreadyExist):
    return JSONResponse(
        status_code=409,
        content={"message": f"Product with name '{exc.product_name}' already exists"}
    )

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong"}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1],
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={"errors": errors}
    )