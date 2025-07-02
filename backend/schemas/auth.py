from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str