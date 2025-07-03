from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, field_validator
class TransactionRequest(BaseModel):
    amt: Decimal = Field(decimal_places = 2)
    description: str = Field(max_length = 100)
    transaction_date : date 
    #Unsure about data validation for both below
    user_id: int #retrieved with dependency function
    category_id: int = Field(gte= 1, lte= 6)
    
    @field_validator("transaction_date")
    @classmethod
    def validate_date(cls, value):
        if value > date.today():
            return ValueError
        return value
    
class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    amt: Decimal = Field(decimal_places = 2)
    description: str = Field(max_length = 100)
    transaction_date : date
    category_name: str 
    