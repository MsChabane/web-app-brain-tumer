from pydantic import BaseModel 
from uuid import UUID
class RadioImageBase(BaseModel):
    type:int
    
    
class RadioImageCreate(RadioImageBase):
    patient_id:UUID
    
    
    