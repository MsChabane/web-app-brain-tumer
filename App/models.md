# User Model (`UserModel.py`)

Represents system users (patients, doctors, or admins) and their relationships.

```python
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime, func
import uuid
from typing import Optional, TYPE_CHECKING
from ..schemas.types import Role
from datetime import datetime

if TYPE_CHECKING:
    from .PatientModel import Patient
    from .DoctorModel import Doctor

class User(SQLModel, table=True):
    __tablename__ = 'user'
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    phone_number: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: Role = Field(default=Role.PATIENT, nullable=False)
    doctor: Optional["Doctor"] = Relationship(back_populates="user")
    patient: Optional["Patient"] = Relationship(back_populates="user")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```
**Key Points:**
*   `id`: Unique UUID primary key.
    
*   `phone_number`: Indexed and unique.
    
*   `password`: Must be hashed before storing.
    
*   `role`: User role (ADMIN, DOCTOR, PATIENT), default is PATIENT.
    
*   `doctor` / `patient`: Optional relationships to Doctor or Patient models.
    
*   `created_at`: Auto-generated timestamp.
    
**Usage Notes:**
*   Controls access permissions based on `role`.
    
*   Relationships allow linking user accounts to specific doctor or patient records.


# Doctor Model (`DoctorModel.py`)

Represents doctors in the system and their relationships to users and patients.

```python
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func
from typing import Optional, List, TYPE_CHECKING
import uuid
from .UserModel import User
from datetime import datetime

if TYPE_CHECKING: 
    from .PatientModel import Patient

class Doctor(SQLModel, table=True):
    __tablename__ = 'doctor'
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, unique=True)
    name: str
    specialty: str
    years_experience: int
    user: Optional[User] = Relationship(back_populates="doctor")
    patients: List["Patient"] = Relationship(back_populates="doctor")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```
**Key Points:**
*   `id`: Unique UUID primary key.
    
*   `user_id`: Links to a `User`, one-to-one relationship.
    
*   `name`, `specialty`, `years_experience`: Doctor information.
    
*   `user`: Relationship to the `User` model.
    
*   `patients`: Relationship to multiple `Patient` records.
    
*   `created_at`: Auto-generated timestamp.
    
**Usage Notes:**
*   Connects user accounts to doctor profiles.
    
*   Tracks which patients are assigned to each doctor.


# Patient Model (`PatientModel.py`)

Represents patients in the system and their relationships to users and doctors.

```python
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime, func
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime
from .UserModel import User
from .DoctorModel import Doctor
from ..schemas.types import Gender, FinalStateEnum, Binary, Four_Classes

class Patient(SQLModel, table=True):
    __tablename__ = "patient"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    age: int = Field()
    gender: Gender = Field()
    antecedents: Four_Classes = Field()
    
    tumor_status: Optional[Binary] = Field(nullable=True, default=None)
    hospitalisation: Optional[Four_Classes] = Field(nullable=True, default=None)
    final_state: Optional[FinalStateEnum] = Field(nullable=True, default=None)

    user_id: UUID = Field(foreign_key="user.id", nullable=False, unique=True)
    user: User = Relationship(back_populates="patient")
    doctor_id: Optional[UUID] = Field(nullable=True, foreign_key="doctor.id")
    doctor: Optional[Doctor] = Relationship(back_populates="patients", sa_relationship_kwargs={"lazy": "joined"})
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```
**Key Points:**
*   `id`: Unique UUID primary key.
    
*   Personal info: `name`, `surname`, `age`, `gender`, `antecedents`.
    
*   Medical info: `tumor_status`, `hospitalisation`, `final_state` (all optional).
    
*   `user_id`: Links to a `User`, one-to-one relationship.
    
*   `doctor_id`: Optional link to a `Doctor`.
    
*   `user` / `doctor`: Relationships for accessing related records.
    
*   `created_at`: Auto-generated timestamp.
    
**Usage Notes:**
*   Connects patient profiles to user accounts and assigned doctors.
    
*   Medical fields can be used for analytics or clinical workflows.


# General Symptoms Model (`GeneralSymptomsModel.py`)

Represents general symptoms reported by patients.

```python
from sqlmodel import SQLModel, Field, Column, DateTime, func
from uuid import uuid4, UUID
from datetime import datetime
from ..schemas.types import Three_Classes, Seizures

class GeneralSymptoms(SQLModel, table=True):
    __tablename__ = "general_symptoms"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    patient_id: UUID = Field(foreign_key="patient.id")
    
    headaches: Three_Classes
    seizures: Seizures
    fatigue: Three_Classes
    drowsiness: Three_Classes
    sleep_pb: Three_Classes
    memory_pb: Three_Classes
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```
**Key Points:**
*   `id`: Unique UUID primary key.
    
*   `patient_id`: Links to the `Patient` model.
    
*   Symptoms tracked: `headaches`, `seizures`, `fatigue`, `drowsiness`, `sleep_pb`, `memory_pb`.
    
*   `created_at`: Timestamp when the record is created.
    
**Usage Notes:**
*   Each record represents a patient’s general symptom assessment.
    
*   Fields use enumerations (`Three_Classes`, `Seizures`) for standardized input.


# Specific Symptoms Model (`SpecificSymptomsModel.py`)

Represents specific symptoms reported by patients.

```python
from sqlmodel import SQLModel, Field, Column, DateTime, func
from uuid import uuid4, UUID
from datetime import datetime
from ..schemas.types import Three_Classes, Four_Classes, Binary

class SpecificSymptoms(SQLModel, table=True):
    __tablename__ = "specific_symptoms"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    patient_id: UUID = Field(foreign_key="patient.id")
    
    pressure: Four_Classes
    balance_loss: Binary
    judgment_degradation: Four_Classes
    sense_degradation: Four_Classes
    lactation: Three_Classes
    swallowing: Four_Classes
    muscle: Four_Classes
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```
**Key Points:**
*   `id`: Unique UUID primary key.
    
*   `patient_id`: Links to the `Patient` model.
    
*   Symptoms tracked: `pressure`, `balance_loss`, `judgment_degradation`, `sense_degradation`, `lactation`, `swallowing`, `muscle`.
    
*   `created_at`: Timestamp when the record is created.
    
**Usage Notes:**
*   Each record represents a patient’s specific symptom assessment.
    
*   Fields use enumerations (`Three_Classes`, `Four_Classes`, `Binary`) for standardized input.