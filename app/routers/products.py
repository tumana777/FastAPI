from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, ProductListResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    category = db.get(Category, product.category_id)

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    existing_product = db.query(Product).filter(Product.name == product.name).first()

    if existing_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists with the same name.")

    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/", response_model=ProductListResponse)
def read_products(page: int | None = 1, page_size: int | None = 10, db: Session = Depends(get_db)):

    total = db.query(Product).count()

    offset = (page - 1) * page_size

    products = db.query(Product).offset(offset).limit(page_size).all()

    return {
        "total": total,
        "items": products,
    }

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product_db = db.get(Product, product_id)

    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    existing_product = db.query(Product).filter(Product.name == product.name).first()

    if existing_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists with the same name.")

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

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}




























