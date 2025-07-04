from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\user\Desktop\trackleh-app\tests\.env.test")
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

from backend.models import Base
from backend.main import app
from backend.database import get_db, get_engine_and_session



TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine, TestingSessionLocal = get_engine_and_session(TEST_DATABASE_URL)
print(TEST_DATABASE_URL)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
