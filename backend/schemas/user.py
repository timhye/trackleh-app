from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length= 6, max_length= 10)
    password: str = Field(min_length = 6, max_length = 10)


class UserResponse(BaseModel):
    id: int 
    username: str = Field(min_length= 6, max_length= 10)
    
class UserProfileRequest(BaseModel):
    username: str 

class UserProfileResponse(BaseModel):
    username: str = Field(min_length= 6, max_length= 10)
    is_active: bool = Field(default = True)
    created_at: datetime 
    updated_at: datetime

