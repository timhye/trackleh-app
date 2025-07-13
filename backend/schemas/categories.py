from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

# Both request and response schemas in the same file

##///////////////////////////////////////
##CategoryRequest will not be used in MVP
##class CategoryRequest(BaseModel):
    ##name: str = Field(..., min_length=1, max_length=50)
from backend.models import TransactionType

    

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    name: str
    transaction_type: TransactionType
    
    #created_at: datetime # Not needed yet unless for future use involving custom categories
    
    ##class Config:(DEPRECATED)
        ##from_attributes = True