from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

# password1 = "otar"
#
# hashed_password = hash_password(password1)

# print(verify_password(password1, hashed_password))
# print(verify_password("otar.", hashed_password))

SECRET_KEY = "secret-oto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# print(create_access_token(data={"user_id": 8}))

# def verify_token(token: str):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#
#     return payload
#
# print(verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE3ODM0MzU4NTl9.OtzIshCSWlB8oTd7o-8QJCBi60nrg_zEVqTJad0okcI"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token invalid or expired")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token invalid or expired")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    return user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    return current_user

















