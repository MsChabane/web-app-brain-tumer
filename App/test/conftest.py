import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock, patch, MagicMock
import uuid

from App.main import app
from App.db.db import get_session
from App.routes.authRoute import user_services
from App.dependancies.auth import AccessTokenChecker, get_current_user
from App.schemas.types import Role
from App.schemas.authSchemas import Token_Data
from App.models.UserModel import User
from App.utils import hash


# -----------------------------------------------------------------
# SESSION FIXTURE
# -----------------------------------------------------------------
@pytest.fixture
def mock_session():
    session = AsyncMock()
    result = MagicMock()
    result.first = AsyncMock(return_value=None)
    session.exec = AsyncMock(return_value=result)
    session.commit = AsyncMock()
    session.delete = AsyncMock()
    session.add = MagicMock()
    return session


@pytest.fixture(autouse=True)
def override_session(mock_session):
    app.dependency_overrides[get_session] = lambda: mock_session
    yield
    app.dependency_overrides.pop(get_session, None)



@pytest.fixture
def override_token_checker():
    async def fake_checker():
        return Token_Data(user_id=str(uuid.uuid4()))

    app.dependency_overrides[AccessTokenChecker.__call__] = fake_checker
    yield
    app.dependency_overrides.pop(AccessTokenChecker.__call__, None)


# -----------------------------------------------------------------
# USERS WITH ROLES
# -----------------------------------------------------------------
def make_user(role: Role):
    return User(
        id=uuid.uuid4(),
        phone_number="0778150652",
        password="hashed",
        role=role,
    )


@pytest.fixture
def client_with_auth_admin(override_token_checker):
    async def fake_user():
        return make_user(Role.ADMIN)

    app.dependency_overrides[get_current_user] = fake_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_current_user, None)



@pytest.fixture
def client_with_auth_doctor(override_token_checker):
    async def fake_user():
        return make_user(Role.DOCTOR)

    app.dependency_overrides[get_current_user] = fake_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def client_with_auth_patient(override_token_checker):
    async def fake_user():
        return make_user(Role.PATIENT)

    app.dependency_overrides[get_current_user] = fake_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_current_user, None)


# -----------------------------------------------------------------
# USER SERVICES PATCHES
# -----------------------------------------------------------------
@pytest.fixture
def fake_login_user():
    fake_user = User(
        id=uuid.uuid4(),
        phone_number="0778150917",
        password=hash("password"),
        role=Role.DOCTOR,
    )

    with patch.object(user_services, "get_by_phone_number", AsyncMock(return_value=fake_user)):
        yield


@pytest.fixture
def fake_user_exist_true():
    with patch.object(user_services, "check_user_exist", AsyncMock(return_value=True)):
        yield


@pytest.fixture
def fake_user_exist_false():
    with patch.object(user_services, "check_user_exist", AsyncMock(return_value=False)):
        yield


@pytest.fixture
def test_client(override_token_checker):
    return TestClient(app)


@pytest.fixture()
def fake_user_list():
    fake_users = [
        {
            "id": str(uuid.uuid4()),
            "phone_number": "0550112233",
            "role": "doctor"
        },
        {
            "id": str(uuid.uuid4()),
            "phone_number": "0660223344",
            "role": "patient"
        }
    ]

    mock = AsyncMock(return_value=fake_users)

    with patch.object(user_services, "get_all", mock):
        yield mock 

