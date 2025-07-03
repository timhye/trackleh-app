from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length= 6, max_length= 10)
    password: str = Field(min_length = 6, max_length = 10)
