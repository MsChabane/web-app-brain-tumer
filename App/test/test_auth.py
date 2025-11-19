import uuid 
from unittest.mock import AsyncMock,MagicMock


def test_login(fake_login_user, test_client):
    data = {
        "phone_number": "0778150917",
        "password": "password"
    }

    response = test_client.post("/auth/login", json=data)
    rs = response.json()

    assert response.status_code == 200
    assert "access_token" in rs
    assert rs.get("role") == "doctor"


def test_create_admin_by_non_admin(client_with_auth_doctor, client_with_auth_patient):
    data = {"phone_number": "077", "password": "pass"}

    # Doctor trying → forbidden
    response = client_with_auth_doctor.post("/auth/create-admin", json=data)
    assert response.status_code == 403
    assert response.json().get("detail") == "Access denied"

    # Patient trying → forbidden
    response = client_with_auth_patient.post("/auth/create-admin", json=data)
    assert response.status_code == 403
    assert response.json().get("detail") == "Access denied"


def test_create_admin_by_admin_with_user_exist(client_with_auth_admin, fake_user_exist_true):
    data = {"phone_number": "0778150614", "password": "pass"}

    response = client_with_auth_admin.post("/auth/create-admin", json=data)
    result = response.json()

    assert response.status_code == 400
    assert result.get("detail") == "User is already exist"


def test_create_admin_by_admin(client_with_auth_admin, fake_user_exist_false):
    data = {"phone_number": "0777847142", "password": "pass"}

    response = client_with_auth_admin.post("/auth/create-admin", json=data)

    assert response.status_code == 201
    


def test_get_all_users_admin(client_with_auth_admin, mock_session, fake_user_list):

    response = client_with_auth_admin.get("/auth/users/all?page=1&limit=2")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    
    fake_user_list.assert_awaited_once_with(
        session=mock_session,
        page=1,
        limit=2
    )

import pytest

def test_profile_patient(client_with_auth_patient):
    response = client_with_auth_patient.post("/auth/profile")
    data = response.json()
    
    assert response.status_code == 200
    assert "id" in data
    assert "phone_number" in data
    assert "role" in data
    assert data["role"] == "patient"


def test_profile_doctor(client_with_auth_doctor):
    response = client_with_auth_doctor.post("/auth/profile")
    data = response.json()
    
    assert response.status_code == 200
    assert "id" in data
    assert "phone_number" in data
    assert "role" in data
    assert data["role"] == "doctor"


def test_profile_admin(client_with_auth_admin):
    response = client_with_auth_admin.post("/auth/profile")
    data = response.json()
    
    assert response.status_code == 200
    assert "id" in data
    assert "phone_number" in data
    assert "role" in data
    assert data["role"] == "admin"
