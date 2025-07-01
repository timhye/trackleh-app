from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Category

router = APIRouter()

@router.get("/")
async def test():
    return "this works perfectly!"