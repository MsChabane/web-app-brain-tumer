from sqlmodel import SQLModel,Field,Relationship
from uuid import uuid4,UUID
from typing  import TYPE_CHECKING    
from ..schemas.types import Three_Classes,Seizures



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
    







