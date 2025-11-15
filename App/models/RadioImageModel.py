from sqlmodel import SQLModel,Field,Column,DateTime,func
from uuid import uuid4,UUID

from datetime import datetime,timezone


from App.models.PatientModel import Patient





class RadioImage(SQLModel, table=True):
    __tablename__ = "radio_image"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type: int
    patient_id: UUID = Field(foreign_key="patient.id")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )