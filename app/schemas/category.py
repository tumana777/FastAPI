from pydantic import BaseModel, Field

class ProductResponseForCategory(BaseModel):
    name: str
    price: float

class CategoryResponse(BaseModel):
    id: int
    name: str
    products: list[ProductResponseForCategory] = []

class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)