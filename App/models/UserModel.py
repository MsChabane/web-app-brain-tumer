from sqlmodel import Field,SQLModel,Relationship
import uuid
from typing import Optional,TYPE_CHECKING,List
from ..schemas.types import Role

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
    patient: List["Patient"] = Relationship(back_populates="user")
    
    

