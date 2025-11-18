from pydantic import BaseModel
from typing import Optional
import uuid

class DoctorBase(BaseModel):
    name:str
    specialty:str
    years_experience:int
    
class DoctorCreate(DoctorBase):
    user_id:uuid.UUID

class DoctorUpdate(BaseModel):
    name : Optional[str]=None
    specialty:Optional[str]=None
    years_experience:Optional[int]=None

class DoctorOut(DoctorBase):
    id :uuid.UUID

    




