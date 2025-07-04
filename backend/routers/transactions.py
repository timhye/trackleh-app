from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from backend.database import get_db
from backend.models import Transactions, Users
from backend.schemas import transactions, user
from backend.utils.dependencies import get_current_user


router = APIRouter()


@router.get("/", response_model = List[transactions.TransactionResponse])
async def get_all_transactions(db: Session = Depends(get_db),
                               current_user: user.UserResponse = Depends(get_current_user)):
    
    #/////DOESNT ALLOW PYTEST TEST TO PASS IF THIS IS UNCOMMENTED
    # try:
    #     txn = Transactions(
    #         amt=400.00,
    #         description="Test Transaction 7",
    #         transaction_date="2025-03-01",
    #         user_id = current_user.id,
    #         category_id = 5,
    #         idempotency_key = "6"

            
    #     )
    #     db.add(txn)
    #     db.commit()
    # except Exception as e:
    #     print(f"Database error: {e}")  # This will show the actual error
    #     raise HTTPException(status_code = 401, detail = f"Entry already sent! Error: {str(e)}")
    
    transaction_list = db.query(Transactions).options(joinedload(Transactions.category)).filter(Transactions.user_id == current_user.id)
    
    response = [
        transactions.TransactionResponse(
            
            id = txn.id,
            amt = txn.amt,
            category_name = txn.category.name,
            description = txn.description,
            transaction_date = txn.transaction_date,
               
        ) for txn in transaction_list
    ]
    
    
    return response

@router.get("/{transaction_id}", response_model = transactions.TransactionResponse)
async def get_specific_transaction(transaction_id : int, db: Session = Depends(get_db),
                             current_user : user.UserResponse = Depends(get_current_user)):
    
    specific_transaction = db.query(Transactions).options(joinedload(Transactions.category)).filter(Transactions.user_id == current_user.id).filter(Transactions.id == transaction_id).first()
    
    if not specific_transaction:
        raise HTTPException(status_code = 404, detail = "Specific Transaction not found")
    
    response = transactions.TransactionResponse(
        
        id = specific_transaction.id,
        amt = specific_transaction.amt,
        category_name = specific_transaction.category.name,
        description = specific_transaction.description,
        transaction_date = specific_transaction.transaction_date
         
    )
    
    # data = transactions.TransactionResponse.model_validate(specific_transaction)
    
    # data["category_name"] = specific_transaction.category.name
    
    # response = transactions.TransactionResponse(**data)
    
    return response
       