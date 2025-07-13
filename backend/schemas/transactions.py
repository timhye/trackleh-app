from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, field_validator

from backend.models import TransactionType


class TransactionRequest(BaseModel):
    amt: Decimal = Field(decimal_places = 2)
    description: str = Field(max_length = 100)
    transaction_date : date 
    type: TransactionType
    #Unsure about data validation for both below
    #user_id: int //retrieved with dependency function
    #idempotency key passed in through header
    category_id: int = Field(gte= 1, lte= 6) #can be passed into the transactionreq obj through client
    ## This is assuming the key and category id is passed in by client
    @field_validator("transaction_date")
    @classmethod
    def validate_date(cls, value):
        if value > date.today():
            raise ValueError("Transaction date cannot be in the future")
        return value
    
class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    amt: Decimal = Field(decimal_places = 2)
    type: TransactionType
    description: str = Field(max_length = 100)
    transaction_date : date
    category_name: str 
    
    
class TransactionFilters(BaseModel):
    days_from_today: Optional[int] = 30
    category: Optional[int] = None
    type: Optional[TransactionType] = None
    search: Optional[str] = None
    
    page: int = Field(1, ge= 1)
    limit: int = Field(20, ge= 1, le= 100)
    
    

    