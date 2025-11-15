from pydantic import BaseModel 
from uuid import UUID
class RadioImageBase(BaseModel):
    type:int
    class Config:
        from_attributes = True
    
    
    
class RadioImageCreate(RadioImageBase):
    patient_id:UUID
    
    
    