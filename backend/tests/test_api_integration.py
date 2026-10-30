import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.models.models import User

# Use a temporary test SQLite file so tables persist across sessions
TEST_DB_PATH = "/tmp/aquamark_test.db"
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"

def test_auth_workflow_and_security():
    # 1. Register Alice
    reg_payload = {
        "email": "alice@faculty.edu",
        "password": "StrongPassword2026!",
        "full_name": "Prof. Alice",
        "institution": "Cryptography Lab"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == "alice@faculty.edu"
    assert user_data["role"] == "admin"  # First registered user is admin

    # 2. Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": "alice@faculty.edu",
        "password": "StrongPassword2026!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token is not None

    # 3. Access authenticated me endpoint
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "alice@faculty.edu"

    # 4. Attempt login with wrong password
    bad_login = client.post("/api/v1/auth/login", json={
        "email": "alice@faculty.edu",
        "password": "WrongPassword123"
    })
    assert bad_login.status_code == 401

def test_unauthorized_access_prevented():
    # Attempt listing documents without token
    res = client.get("/api/v1/documents")
    assert res.status_code == 401
