from pydantic import BaseModel,Field
from uuid import UUID
from App.schemas.common import Gender,FinalStateEnum,Binary,Four_Classes

class PatientBase(BaseModel):
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    age: int =Field()
    gender: Gender =Field()

class PatientCreate(PatientBase):
    user_id:UUID
    
    
    
    

    

