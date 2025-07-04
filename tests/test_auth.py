import os

import pytest

from tests.conftest import TEST_DATABASE_URL




# @pytest.fixture
# def get_auth_headers(client):
#     response = client.post("/auth/login", json={"username": "test", "password": "test"})
#     token = response.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}



def test_register_existing_user(client, db_session):
    from backend.models import Users
    user = Users(username = "jonjon")
    db_session.add(user)
    db_session.commit()
    
    response = client.post("/auth/register/", json = {
        "username": "jonjon",
        "password": "snowing"
    })
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username is already registered"
    
def test_register_new_user(client, db_session):
    
    #Empty initial test database, so registration should go through
    
    response = client.post("/auth/register/", json = {
        "username": "jonjon",
        "password": "snowing"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User created successfully"
    
def test_invalid_username(client, db_session):
    
    #Assume no duplicate of username
    
    response = client.post("/auth/register/", json = {
        "username": "jon",
        "password": "snowing"
    })
    
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "String should have at least 6 characters"
    
    
def test_using_test_db():
    assert TEST_DATABASE_URL != os.getenv("DATABASE_URL")
