from sqlmodel import SQLModel,Field,Column,DateTime,func

from uuid import uuid4,UUID
   
from ..schemas.types import Three_Classes,Seizures
from datetime import datetime 




class GeneralSymptoms(SQLModel, table=True):
    __tablename__ = "general_symptoms"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    patient_id: UUID = Field(foreign_key="patient.id")
    
    headaches:Three_Classes
    seizures:Seizures 
    fatigue: Three_Classes
    drowsiness: Three_Classes
    sleep_pb: Three_Classes
    memory_pb: Three_Classes
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )






