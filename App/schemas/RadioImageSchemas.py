from pydantic import BaseModel ,ConfigDict
from uuid import UUID
from datetime import datetime
class RadioImageBase(BaseModel):
    type:int
    
    
    
    
class RadioImageCreate(RadioImageBase):
    patient_id:UUID
    
class RadioImageOut(RadioImageBase):
    id:UUID
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)
    
