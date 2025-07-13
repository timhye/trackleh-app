from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from backend.database import get_db
from backend.models import Users
from backend.schemas import UserCreate, Token
from backend.utils.auth_utils import hash_password, verify_password, create_access_token



router = APIRouter()

@router.post("/register", status_code = status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Username is already registered"
        )
    hashed_password = hash_password(user.password)
    new_user = Users(username = user.username, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


@router.post("/login" , response_model = Token)
async def login_user(
    form_data : OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
        user = db.query(Users).filter(Users.username == form_data.username).first()

        if not user or not verify_password(form_data.password, user.hashed_password):
             raise HTTPException(
                  status_code = status.HTTP_401_UNAUTHORIZED,
                  detail = "Incorrect username or password",
                  headers = {"WWWW-Authenticate": "Bearer"}
             )
        
        access_token = create_access_token(data = {"sub": str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"}
            