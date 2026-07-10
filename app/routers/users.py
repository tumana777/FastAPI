from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.services import send_email, write_log

from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate
from app.database import get_db
from app.models.user import User
from app.security import (
    hash_password, verify_password, create_access_token,
    oauth2_scheme, get_current_user, require_admin
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, background_task: BackgroundTasks, db: Session = Depends(get_db)):
    existing_user_username = db.query(User).filter(User.username == user.username).first()

    if existing_user_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists")

    existing_user_email = db.query(User).filter(User.email == user.email).first()

    if existing_user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")

    hashed_password = hash_password(user.password)

    data = user.model_dump(exclude={"password"})

    new_user = User(**data, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # send_email(new_user.email)
    # write_log(new_user.username)

    background_task.add_task(send_email, new_user.email)
    background_task.add_task(write_log, new_user.username)

    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")


    token = create_access_token(data={"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# @router.get("/me")
# def get_me(token: str = Depends(oauth2_scheme)):
#     print(token)
#
#     return {"token": token}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me")
def update_me(user: UserUpdate,
              current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)
):
    existing_username = db.query(User).filter(User.username == user.username).first()

    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    data = user.model_dump(exclude_unset=True, exclude={"password"})

    hashed_password = hash_password(user.password) if user.password else current_user.hashed_password

    current_user.hashed_password = hashed_password

    print(data)

    for field, value in data.items():
        setattr(current_user, field, value)

    db.commit()

    return {
        "message": "Profile updated",
    }

@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    users = db.query(User).all()

    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}

@router.patch("/{user_id}/make_admin")
def make_admin(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already an admin")

    user.role = "admin"

    db.commit()
    return {"message": f"User - {user.username} is now an admin"}

@router.patch("/{user_id}/remove_admin")
def remove_admin(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.role == "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already an user")

    if current_user.id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot remove admin privileges from yourself")

    user.role = "user"

    db.commit()

    return {"message": f"User - {user.username} is now an user"}
























