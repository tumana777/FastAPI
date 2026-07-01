from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session, selectinload
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).options(selectinload(Category.products)).order_by(Category.id.desc()).all()

    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)

    return category

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):

    existing_category = db.query(Category).filter(Category.name == category.name).first()

    if existing_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists with the same name.")

    new_category = Category(name=category.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.put("/{category_id}")
def update_category(category_id: int, new_category: CategoryCreate, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category.name = new_category.name
    db.commit()
    db.refresh(category)

    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    # if category.products:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete a category with associated products.")

    db.delete(category)
    db.commit()

    return {"message": "Category deleted"}
