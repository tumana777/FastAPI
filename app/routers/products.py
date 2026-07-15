from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import get_db, get_async_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, ProductListResponse
from sqlalchemy import select, func
from app.exceptions import ProductNotFound, ProductAlreadyExist

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    category = db.get(Category, product.category_id)

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    existing_product = db.query(Product).filter(Product.name == product.name).first()

    if existing_product:
        raise ProductAlreadyExist(product_name=product.name)

    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# @router.get("/", response_model=ProductListResponse)
# def read_products(page: int | None = 1, page_size: int | None = 10, db: Session = Depends(get_db)):
#
#     total = db.query(Product).count()
#
#     offset = (page - 1) * page_size
#
#     products = db.query(Product).offset(offset).limit(page_size).all()
#
#     return {
#         "total": total,
#         "items": products,
#     }

@router.get("/", response_model=ProductListResponse)
async def read_products(page: int | None = 1, page_size: int | None = 10, db: AsyncSession = Depends(get_async_db)):

    total_products = await db.execute(select(func.count()).select_from(Product))

    total = total_products.scalar()

    offset = (page - 1) * page_size

    products = await db.execute(select(Product).offset(offset).limit(page_size))

    products = products.scalars().all()

    return {
        "total": total,
        "items": products,
    }

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if not product:
        raise ProductNotFound()

    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product_db = db.get(Product, product_id)

    if not product_db:
        raise ProductNotFound()

    existing_product = db.query(Product).filter(Product.name == product.name).first()

    if existing_product:
        raise ProductAlreadyExist(product_name=product.name)

    if product.category_id is not None:
        category = db.get(Category, product.category_id)

        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    data = product.model_dump(exclude_unset=True).items()

    for field, value in data:
        setattr(product_db, field, value)

    db.commit()
    db.refresh(product_db)

    return product_db

@router.patch("/{product_id}")
def update_product_price(product_id: int, new_price: float, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if not product:
        raise ProductNotFound()

    old_data = {
        "price": product.price,
        "updated_at": datetime.now()
    }

    encoded_data = jsonable_encoder(old_data)

    product.price = new_price

    db.commit()

    return JSONResponse(status_code=200, content=encoded_data)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if not product:
        raise ProductNotFound()

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}




























