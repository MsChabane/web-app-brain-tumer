from sqlmodel import  SQLModel,Field,Relationship
from typing import Optional,List,TYPE_CHECKING
import uuid
from .UserModel import User
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
