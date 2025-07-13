from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

from jose import JWTError, jwt
from passlib.context import CryptContext



##Loading variables needed for encoding JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

##Password hashing and validation functionality
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)  # Creates irreversible bcrypt hash

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)  # Securely compares passwords



# JWT token handling functionality
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()    
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    try:
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"  - Token created successfully: {token[:50]}...")
        return token
    except Exception as e:
        print(f"  - TOKEN CREATION FAILED: {e}")
        raise

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Verify signature and expiration
        return payload
    except JWTError:
        return None
