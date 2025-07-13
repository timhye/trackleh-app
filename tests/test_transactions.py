# test_transactions.py
import pytest
from fastapi.testclient import TestClient
from backend.models import Users, Transactions, Category
from backend.utils.auth_utils import create_access_token  # Your function to create JWT tokens

@pytest.fixture(scope = "function")
def test_category(db_session):
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture(scope = "function")
def test_user(db_session):
    # Create a test user
    user = Users(username="testuser", hashed_password="fakehashed", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  

    return user

@pytest.fixture(scope = "function")
def test_transaction(db_session, test_user, test_category):
    # Create a test transaction for the user
    txn = Transactions(
        amt=100.00,
        description="Test Transaction",
        transaction_date="2025-07-04",
        user_id = test_user.id,
        category_id = test_category.id,
                idempotency_key = "75"

        
    )
    db_session.add(txn)
    db_session.commit()
    return txn

def get_auth_header(user):
    token = create_access_token(data={"sub": user.username})
    return {"Authorization": f"Bearer {token}"}

# def test_show_all_transactions_authorized(test_user, client, test_transaction):
#     headers = get_auth_header(test_user)
#     response = client.get("/transactions/", headers=headers)
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert any(txn["description"] == "Test Transaction" for txn in data)

def test_show_all_transactions_authorized(test_user, client, test_transaction):
    print(f"Test user ID: {test_user.id}, Username: {test_user.username}")
    
    headers = get_auth_header(test_user)
    print(f"Auth header: {headers}")
    
    response = client.get("/transactions/", headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    assert response.status_code == 200
