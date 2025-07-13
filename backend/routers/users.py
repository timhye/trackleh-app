from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from backend.database import get_db
from backend.models import Users
from backend.schemas import user
from backend.utils.dependencies import get_current_user


router = APIRouter()

@router.get("/", status_code = status.HTTP_201_CREATED)
async def get_user_details(current_user: user.UserProfileResponse = Depends(get_current_user)):
    return current_user

@router.put("/")
async def update_user_details(input: user.UserProfileRequest,
                              db: Session = Depends(get_db),
                              current_user: Users = Depends(get_current_user)):
    if input.username:
        # Check if username already exists (excluding current user)
        existing_user = db.query(Users).filter(
            Users.username == input.username,
            Users.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail="Username already exists"
            )
        
        # Update the username
        current_user.username = input.username
    
    # Commit changes and refresh
    db.commit()
    db.refresh(current_user)
    
    user_details = user.UserProfileResponse(username = current_user.username,
                                            is_active = current_user.is_active,
                                            created_at = current_user.created_at,
                                            updated_at = current_user.updated_at)
    
    return user_details

        
        