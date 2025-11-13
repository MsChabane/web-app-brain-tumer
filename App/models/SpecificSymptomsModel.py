from sqlmodel import SQLModel,Field,Relationship
from uuid import uuid4,UUID

from  ..schemas.types import Three_Classes,Four_Classes,Binary






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
    



