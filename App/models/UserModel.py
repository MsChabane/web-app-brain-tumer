from sqlmodel import Field,SQLModel,Relationship,Column,DateTime,func

import uuid
from typing import Optional,TYPE_CHECKING,List
from ..schemas.types import Role
from datetime import datetime ,timezone

if TYPE_CHECKING:
    from .PatientModel import Patient
    from .DoctorModel import Doctor



class User(SQLModel, table=True):
    __tablename__='user'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    phone_number: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: Role = Field(default=Role.PATIENT,nullable=False)
    doctor: Optional["Doctor"] = Relationship(back_populates="user")
    patient: Optional["Patient"] = Relationship(back_populates="user")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    

