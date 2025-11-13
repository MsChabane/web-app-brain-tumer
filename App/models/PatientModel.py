from sqlmodel import Field,SQLModel,Relationship
from .UserModel import User
from uuid import uuid4,UUID
from typing import Optional

from .DoctorModel import Doctor
from ..schemas.common import Gender,FinalStateEnum,Binary,Four_Classes


class Patient(SQLModel, table=True):
    __tablename__ = "patient"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    age: int =Field()
    gender: Gender =Field()

    
    antecedents: Optional[Four_Classes] = Field(nullable=True)
    tumor_status: Optional[Binary] = Field(nullable=True)
    hospitalisation: Optional[Four_Classes] = Field(nullable=True)
    final_state: Optional[FinalStateEnum] = Field(nullable=True)

    user_id: UUID = Field(foreign_key="user.id", nullable=False,unique=True)
    user: User = Relationship(back_populates="patient")
    doctor_id: Optional[UUID] = Field(nullable=True, foreign_key="doctor.id")
    doctor: Optional[Doctor] = Relationship(back_populates="patients")
