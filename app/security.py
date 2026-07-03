from pwdlib import PasswordHash
from jose import jwt
from datetime import datetime, timedelta

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

print(create_access_token(data={"id":1}))
