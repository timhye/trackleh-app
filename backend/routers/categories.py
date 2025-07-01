from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import categories
import models

router = APIRouter()

@router.get("/", response_model = List[categories.CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories
    
@router.get("/{category_id}", response_model = categories.CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found")
    return category

"""NOTE: Create, Update and Delete operations for categories will not be implemented in the mvp first iteration 
as they are low priority features compared to the rest of the CRUD operations for auth and transactions as our 
categories for now are seeded so we will only require these missing CRUD operations in later iterations when we
start to allow for custom category creation, modification and deletion """
