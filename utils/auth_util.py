import os, bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def encrypt_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def generate_token(
    username: str, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
):
    data = {"sub": username}
    expires = datetime.now(timezone.utc) + timedelta(minutes=int(expires_delta))
    data |= {"exp": expires}
    
    return jwt.encode(data, SECRET_KEY, ALGORITHM)

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])