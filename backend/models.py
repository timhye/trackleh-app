import enum

from sqlalchemy import Column, Integer, String, Boolean, Float, DECIMAL, DateTime, Date, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base


class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    
    
class Users(Base):
    __tablename__ = 'users'

    #some attributes will be left out for this mvp
    id = Column(Integer, primary_key = True)
    #firstname = Column(String)
    #lastname = Column(String)
    username = Column(String, unique = True) ##Might be changed to email in the future or might just add new col
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)
    #role = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())
    
    transactions = relationship("Transactions", back_populates="user")




class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key = True)
    amt = Column(DECIMAL(12,2))
    type = Column(
        Enum(TransactionType, values_callable=lambda x: [e.value for e in x]),
        nullable=False, 
        index=True)
    description = Column(String)
    transaction_date = Column(Date, index = True)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now()) ##onupdate to update timestamp automatically when record is modified
    user_id = Column(Integer, ForeignKey('users.id'), index = True)
    category_id = Column(Integer, ForeignKey('categories.id'), index = True)
    idempotency_key = Column(String, nullable= False)  ## To be generated and given by client

    user = relationship("Users", back_populates = "transactions")
    
    category = relationship("Category", back_populates = "transactions")
    
    __table_args__ = (
        UniqueConstraint('user_id','idempotency_key',name = 'uq_user_idempotency'),
    )


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    name = Column(String, unique = True)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    transactions = relationship("Transactions", back_populates = "category")