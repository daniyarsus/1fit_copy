import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


valid_register_data = {
    "username": "testuser",
    "password": "testpassword",
    "email": "test@example.com",
    "phone": 1234567890
}

valid_login_username_data = {
    "username": "testuser",
    "password": "testpassword"
}

valid_login_email_data = {
    "email": "test@example.com",
    "password": "testpassword"
}

valid_login_phone_data = {
    "phone": 1234567890,
    "password": "testpassword"
}

valid_logout_data = {
    "jwt": "valid_jwt_token"
}


def test_register_user():
    response = client.post("/api/v1/signup/register", json=valid_register_data)
    assert response.status_code == 200
    assert "username" in response.json()
    assert "email" in response.json()
    assert "phone" in response.json()


def test_send_code():
    response = client.post("/api/v1/signup/send-code", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_verify_code():
    response = client.post("/api/v1/signup/verify-code", json={"email": "test@example.com", "code": 123456})
    assert response.status_code == 200
    assert "message" in response.json()


def test_login_username():
    response = client.post("/api/v1/signin/token-username", json=valid_login_username_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_email():
    response = client.post("/api/v1/signin/token-email", json=valid_login_email_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_phone():
    response = client.post("/api/v1/signin/token-phone", json=valid_login_phone_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_update_refresh_token():
    response = client.post("/api/v1/signin/update-refresh-token", json={"jwt": "valid_jwt_token"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_change_password_send_code():
    response = client.post("/api/v1/password/send-code", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_change_password_verify_code():
    response = client.post("/api/v1/password/verify-code", json={"email": "test@example.com", "code": 123456, "new_password": "newpassword"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_logout_user():
    response = client.post("/api/v1/logout/del-token", json=valid_logout_data)
    assert response.status_code == 200
    assert "message" in response.json()


def test_protected_resource():
    response = client.get("/api/v1/protected")
    assert response.status_code == 401
