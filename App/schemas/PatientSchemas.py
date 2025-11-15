from pydantic import BaseModel,Field
from uuid import UUID
from .types import Gender,Four_Classes,Binary,FinalStateEnum
from typing import Optional,TYPE_CHECKING


    

class PatientBase(BaseModel):
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    age: int =Field()
    gender: Gender =Field()
    antecedents: Four_Classes
    
    

   

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
    tumor_status: Binary |None
    hospitalisation: Four_Classes |None
    final_state: FinalStateEnum |None
    

    

