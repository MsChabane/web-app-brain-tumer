from sqlmodel import Field,SQLModel,Relationship,Column,DateTime,func

from .UserModel import User
from uuid import uuid4,UUID
from typing import Optional,TYPE_CHECKING,List
from datetime import datetime,timezone
from ..schemas.types import Gender,FinalStateEnum,Binary,Four_Classes
from .DoctorModel import Doctor

class Patient(SQLModel, table=True):
    __tablename__ = "patient"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    age: int =Field()
    gender: Gender =Field()
    antecedents: Four_Classes= Field()

    
    tumor_status: Optional[Binary] = Field(nullable=True,default=None)
    hospitalisation: Optional[Four_Classes] = Field(nullable=True,default=None)
    final_state: Optional[FinalStateEnum] = Field(nullable=True,default=None)

    user_id: UUID = Field(foreign_key="user.id", nullable=False,unique=True)
    user: User = Relationship(back_populates="patient")
    doctor_id: Optional[UUID] = Field(nullable=True, foreign_key="doctor.id")
    doctor: Optional[Doctor] = Relationship(back_populates="patients")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )