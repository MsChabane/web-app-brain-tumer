import uuid
import pytest
from unittest.mock import AsyncMock, patch,Mock

from App.schemas.types import Role
from App.models.UserModel import User
from App.models.PatientModel import Patient
from App.routes.authRoute import user_services
from App.routes.patientRoute import patient_services


# ---------------------------------------------------
# Helper Fake Objects
# ---------------------------------------------------
def make_fake_user():
    return User(
        id=uuid.uuid4(),
        phone_number="0555123456",
        password="hashed",
        role=Role.PATIENT
    )


def make_fake_patient(user_id):
    return Patient(
        id=uuid.uuid4(),
        user_id=user_id,
        full_name="Test Patient",
        age=25
    )



@pytest.fixture
def new_patient_payload():
    return {
        "user": {
            "phone_number": "0777888999"
        },
        "patient": {
            "name": "Test Patient",
            'surname':'Test',
            "age": 25,
            "gender":'F',
            'antecedents':0
        }
    }




        

        


def test_create_patient_user_already_exists(
    client_with_auth_admin,
    new_patient_payload
):
    existing_user = make_fake_user()

    with patch.object(user_services, "get_by_phone_number", AsyncMock(return_value=existing_user)):

        response = client_with_auth_admin.post("/patient/new-patient", json=new_patient_payload)

        assert response.status_code == 400
        assert response.json()["detail"] == "User is already found."

def test_create_patient_forbidden(client_with_auth_doctor, new_patient_payload):
    
    response = client_with_auth_doctor.post("/patient/new-patient", json=new_patient_payload)

    assert response.status_code == 403
