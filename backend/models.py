from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DECIMAL, DateTime, Date, ForeignKey
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique = True) ##Might be changed to email in the future or might just add new col
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)
    role = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())



class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key = True)
    amt = Column(DECIMAL(12,2))
    description = Column(String)
    transaction_date = Column(Date, index = True)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now()) ##onupdate to update timestamp automatically when record is modified
    user_id = Column(Integer, ForeignKey('users.id'), index = True)
    category_id = Column(Integer, ForeignKey('categories.id'), index = True)



class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    name = Column(String, unique = True)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

