from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session, joinedload

from backend.database import get_db
from backend.models import Transactions, Users, Category
from backend.schemas import transactions, user
from backend.utils.dependencies import get_current_user


router = APIRouter()


@router.get("/search")
async def get_filtered_transactions(db: Session = Depends(get_db),
                                    current_user: user.UserResponse = Depends(get_current_user),
                                    filters: transactions.TransactionFilters = Depends()):

    query = db.query(Transactions).filter(Transactions.user_id == current_user.id)
     
    if filters.days_from_today:
        cutoff_date = datetime.now() - timedelta(days = filters.days_from_today )
        query = query.filter(Transactions.transaction_date >= cutoff_date)
         
    if filters.category:
        query = query.filter(Transactions.category_id == filters.category)

    if filters.type:
        query = query.filter(Transactions.type == filters.type)
        
    if filters.search:
        query = query.filter(Transactions.description.ilike(f"%{filters.search}%"))
        
    total_count = query.count()
    
    query = query.order_by(Transactions.transaction_date.desc())
    offset = (filters.page - 1) * filters.limit
    result = query.offset(offset).limit(filters.limit).all()

    total_pages = (total_count + filters.limit - 1) // filters.limit
    
    has_next = filters.page < total_pages
    
    has_prev = filters.page > 1
    
    response = [
        transactions.TransactionResponse(
            
            id = txn.id,
            amt = txn.amt,
            type = txn.type,
            category_name = txn.category.name,
            description = txn.description,
            transaction_date = txn.transaction_date,
               
        ) for txn in result
    ]
    
    return {
        "transactions": response,
        "pagination": {
            "current_page": filters.page,
            "total_pages": total_pages,
            "total_count": total_count,
            "has_next": has_next,
            "has_prev": has_prev,
            "page_size": filters.limit
        }
    }
    
            
        
@router.get("/", response_model = List[transactions.TransactionResponse])
async def get_all_transactions(db: Session = Depends(get_db),
                               current_user: user.UserResponse = Depends(get_current_user)):
    
    #/////DOESNT ALLOW PYTEST TEST TO PASS IF THIS IS UNCOMMENTED
    # try:
    #     txn = Transactions(
    #         amt=4000.00,
    #         type = "expense",
    #         description="Test Transaction 69",
    #         transaction_date="2026-07-01",
    #         user_id = current_user.id,
    #         category_id = 2,
    #         idempotency_key = "3695"

            
    #     )
    #     db.add(txn)
    #     db.commit()
    # except Exception as e:
    #     print(f"Database error: {e}")  # This will show the actual error
    #     raise HTTPException(status_code = 401, detail = f"Entry already sent! Error: {str(e)}")
    #//////////////////////////
    transaction_list = db.query(Transactions).options(joinedload(Transactions.category)).filter(Transactions.user_id == current_user.id).order_by(Transactions.transaction_date.desc()).all()
    
    response = [
        transactions.TransactionResponse(
            
            id = txn.id,
            amt = txn.amt,
            type = txn.type,
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
        type = specific_transaction.type,
        category_name = specific_transaction.category.name,
        description = specific_transaction.description,
        transaction_date = specific_transaction.transaction_date
         
    )
    
    # data = transactions.TransactionResponse.model_validate(specific_transaction)
    
    # data["category_name"] = specific_transaction.category.name
    
    # response = transactions.TransactionResponse(**data)
    
    return response
       

@router.post("/")
async def create_transaction(entry: transactions.TransactionRequest,
                             idempotency_key: str = Header(...,alias="Idempotency-Key"),
                             db: Session = Depends(get_db),
                             current_user: user.UserResponse = Depends(get_current_user)
                             ):
    
    existing_transaction = db.query(Transactions).filter(
        Transactions.user_id == current_user.id,
        Transactions.idempotency_key  == idempotency_key
    ).first()
    
    if existing_transaction:
        return existing_transaction#idempotent behavior

    check = db.query(Category).filter(Category.id == entry.category_id).first()
    if check.transaction_type != entry.type:
        raise HTTPException(status_code = 422, detail = "Mismatch of category and transaction type")
    
    try:
        submission = Transactions(
            amt = entry.amt,
            type = entry.type,
            description = entry.description,
            user_id = current_user.id,
            category_id = entry.category_id,
            transaction_date = entry.transaction_date,
            idempotency_key = idempotency_key
            ##Keep in mind idempotency key and category id is to be generated and passed in byclient
        )
    
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission
    
    except Exception as e:
        print(f"Database error: {e}")  # This will show the actual error
        raise HTTPException(status_code = 400, detail = "Error in logging transaction")
        
@router.put("/{transaction_id}")
async def update_transaction(
                             entry: transactions.TransactionRequest,
                             transaction_id: int,
                             db: Session = Depends(get_db),
                             current_user: user.UserResponse = Depends(get_current_user)
):
    existing_transaction = db.query(Transactions).filter(current_user.id == Transactions.user_id, transaction_id == Transactions.id).first()
    
    if not existing_transaction:
        raise HTTPException(status_code = 404, detail = "Transaction not found")
    
    check = db.query(Category).filter(Category.id == entry.category_id).first()
    if check.transaction_type != entry.type:
        raise HTTPException(status_code = 422, detail = "Mismatch of category and transaction type")
    
    try:
            existing_transaction.amt = entry.amt
            existing_transaction.description = entry.description
            existing_transaction.transaction_date = entry.transaction_date
            existing_transaction.type = entry.type
            existing_transaction.category_id = entry.category_id
            existing_transaction.updated_at = datetime.now(timezone.utc)
            
            db.commit()
            db.refresh(existing_transaction)
            
            return existing_transaction
    
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code = 401, detail = "Transaction not found")
                

    
@router.delete("/{transaction_id}")
async def delete_transaction(
                              transaction_id: int,
                              db: Session = Depends(get_db),
                              current_user: user.UserResponse = Depends(get_current_user)
                                
):
    delete_count = db.query(Transactions).filter(transaction_id == Transactions.id, current_user.id == Transactions.user_id).delete()
    if not delete_count:
        raise HTTPException(status_code = 404, detail = "Transaction not found")
    
    db.commit()
    return {"message": "Transaction deleted successfully"}
    
