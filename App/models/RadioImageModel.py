from sqlmodel import SQLModel,Field,Relationship
from uuid import uuid4,UUID






class RadioImage(SQLModel, table=True):
    __tablename__ = "radio_images"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type: int
    patient_id: UUID = Field(foreign_key="patient.id",unique=True)
    
