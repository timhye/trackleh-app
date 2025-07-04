import os
from dotenv import load_dotenv
load_dotenv(dotenv_path = r"C:\Users\user\Desktop\trackleh-app\backend\.env")

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker



def get_engine_and_session(database_url=None):
    if database_url is None:
        database_url = os.getenv("DATABASE_URL")
        print(database_url)
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

engine, SessionLocal = get_engine_and_session()

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
