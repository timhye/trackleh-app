from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Transactions
#from schemas import TransactionCreate, TransactionResponse

router = APIRouter()


@router.get("/")
async def test():
    return "This works perfectly!"