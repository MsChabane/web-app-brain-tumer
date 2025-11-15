from sqlmodel import  SQLModel,Field,Relationship,Column,DateTime,func
from typing import Optional,List,TYPE_CHECKING
import uuid
from .UserModel import User
from datetime import datetime ,timezone

if TYPE_CHECKING: 
    from .PatientModel import Patient


class Doctor(SQLModel, table=True):
    __tablename__='doctor'
    id:uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False,unique=True)
    name:str
    specialty: str
    years_experience: int 
    user: Optional[User] = Relationship(back_populates="doctor")
    patients: List["Patient"] = Relationship(back_populates="doctor")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )