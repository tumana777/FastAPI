from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    stock: int | None = Field(default=0, ge=0)
    is_available: bool | None = Field(default=True)
    description: str | None = Field(default=None, min_length=3, max_length=255)
    category_id: int



class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int | None
    is_available: bool | None
    description: str | None
    category_id: int

class ProductListResponse(BaseModel):
    total: int
    items: list[ProductResponse]

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    is_available: bool | None = None
    description: str | None = Field(default=None, min_length=3, max_length=255)
    category_id: int | None = None