from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import categories, user
from backend import models
from backend.utils.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model = List[categories.CategoryResponse])
async def get_categories(type: Optional[str] = Query(None, regex="^(income|expense)$"),
                         db: Session = Depends(get_db),
                         current_user : user.UserResponse = Depends(get_current_user)):
    
    categories = db.query(models.Category)
    
    if type:
        categories = categories.filter(models.Category.transaction_type == type)
    
    response = categories.all()
    
    return response
    
@router.get("/{category_id}", response_model = categories.CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db),
                       current_user : user.UserResponse = Depends(get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found")
    return category

"""NOTE: Create, Update and Delete operations for categories will not be implemented in the mvp first iteration 
as they are low priority features compared to the rest of the CRUD operations for auth and transactions as our 
categories for now are seeded so we will only require these missing CRUD operations in later iterations when we
start to allow for custom category creation, modification and deletion """
