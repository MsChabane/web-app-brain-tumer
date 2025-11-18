
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock,patch
import uuid

from App.main import app
from App.db.db import get_session
from App.routes.authRoute import user_services
from App.models.UserModel import User
from App.schemas.types import Role


mock_session = Mock()
mock_user_services = Mock()

async def get_mock_session():
    yield mock_session

app.dependency_overrides[get_session] = get_mock_session

@pytest.fixture
def fake_session():
    return mock_session



@pytest.fixture
def mock_checkpwd():
    with patch("App.routes.authRoute.checkpwd", return_value=True) as mock:
        yield mock

@pytest.fixture
def fake_user_services():
    
    fake_user = User(
        id=uuid.uuid4(),
        phone_number="45",
        password="hashedpassword",  
        role=Role.DOCTOR
    )
   
    mock_user_services.get_by_phone_number = AsyncMock(return_value=fake_user)
    
    
    user_services.get_by_phone_number = mock_user_services.get_by_phone_number
    return mock_user_services


@pytest.fixture
def test_client():
    return TestClient(app)
