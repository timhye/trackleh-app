from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

# Both request and response schemas in the same file

##///////////////////////////////////////
##CategoryRequest will not be used in MVP
##class CategoryRequest(BaseModel):
    ##name: str = Field(..., min_length=1, max_length=50)

    

class CategoryResponse(BaseModel):
    id: int
    name: str
    #created_at: datetime # Not needed yet unless for future use involving custom categories
    
    class Config:
        from_attributes = True