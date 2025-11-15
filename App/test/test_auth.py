
def test_login(fake_session, fake_user_services,mock_checkpwd, test_client):
    data = {
        "phone_number": "45",
        "password": "password"
    }
    
    response = test_client.post("/auth/login", json=data)
    
    rs=response.json()
    assert response.status_code == 200
    assert "access_token" in rs
    assert 'role' in rs and rs.get("role")=='doctor'
