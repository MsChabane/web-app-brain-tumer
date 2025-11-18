from pydantic import BaseModel,Field,field_validator
from uuid import UUID
from .types import Gender,Four_Classes,Binary,FinalStateEnum
from typing import Optional


    

class PatientBase(BaseModel):
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    age: int =Field()
    gender: Gender =Field()
    antecedents: Four_Classes
    
    @field_validator("age")
    def validate_age(cls,age):
        if age<=0 or age >130:
            raise ValueError("Invalid age value")
        return age 
            

   

class PatientCreate(PatientBase):
    user_id:UUID
    
class PatientUpdateStatus(BaseModel):
    tumor_status: Binary |None
    hospitalisation: Four_Classes |None
    final_state: FinalStateEnum |None
    
class PatientUpdate(BaseModel):
    name: Optional[str] =None
    surname: Optional[str] =None
    age: Optional[int]=None 
    gender: Optional[Gender] =None
    antecedents: Optional[Four_Classes]=None
    
class PatientOut(PatientBase):
    id:UUID
    tumor_status: Binary |None
    hospitalisation: Four_Classes |None
    final_state: FinalStateEnum |None
    

    

