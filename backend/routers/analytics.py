from datetime import date, datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from backend.database import get_db
from backend.models import Transactions, Users, TransactionType, Category
from backend.schemas import transactions, user
from backend.utils.dependencies import get_current_user

router = APIRouter()


@router.get("/")
async def get_analytics_summary(
    start_date: Optional[date] = Query(None, description = "Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description = "End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: user.UserResponse = Depends(get_current_user)
):
    if not start_date:
        start_date = datetime.now().replace(day = 1).date()
        
    if not end_date:
        if datetime.now().month == 12:
            end_date = datetime.now().replace(year = datetime.now().year + 1, month = 1, day = 1).date()
        else:
            end_date = datetime.now().replace(month = datetime.now().month + 1, day = 1).date()
    
    ##Total income earned in a date range
    total_income = db.query(func.sum(Transactions.amt)).filter(
        Transactions.user_id == current_user.id,
        Transactions.type == TransactionType.INCOME,
        Transactions.transaction_date >= start_date,
        Transactions.transaction_date < end_date
    ).scalar() or 0
    
    ##Total expense spent in a specified date range
    total_expense = db.query(func.sum(Transactions.amt)).filter(
        Transactions.user_id == current_user.id,
        Transactions.type == TransactionType.EXPENSE,
        Transactions.transaction_date >= start_date,
        Transactions.transaction_date < end_date
    ).scalar() or 0
    
    top_categories = db.query(
    Category.name,
    func.sum(Transactions.amt).label('total')
    ).join(Transactions).filter(
        Transactions.user_id == current_user.id,
        Transactions.type == TransactionType.EXPENSE,
        Transactions.transaction_date >= start_date,
        Transactions.transaction_date < end_date
    ).group_by(Category.name).order_by(func.sum(Transactions.amt).desc()).limit(3).all()

    # Transaction count
    transaction_count = db.query(Transactions).filter(
        Transactions.user_id == current_user.id,
        Transactions.transaction_date >= start_date,
        Transactions.transaction_date < end_date,
        
    ).count()
    
    return {
    "total_income_current_month": float(total_income),
    "total_expenses_current_month": float(total_expense),
    "net_income_current_month": float(total_income - total_expense),
    "top_spending_categories": [
        {"name": cat.name, "amount": float(cat.total)} 
        for cat in top_categories
    ],
    "transaction_count_for_time_period": transaction_count
}
