from pydantic import BaseModel
from uuid import UUID
from .types import Three_Classes,Four_Classes,Binary
from typing import Optional


class SpecificSymptomsBase(BaseModel):
    pressure: Four_Classes
    balance_loss: Binary
    judgment_degradation: Four_Classes
    sense_degradation: Four_Classes
    lactation: Three_Classes
    swallowing: Four_Classes
    muscle: Four_Classes
    
    
class SpecificSymptomsCreate(SpecificSymptomsBase):
    patient_id:UUID
    
class SpecificSymptomsOut(SpecificSymptomsBase):
    id:UUID
    
    
class SpecificSymptomsUpdate(BaseModel):
    pressure: Optional[Four_Classes]=None
    balance_loss: Optional[Binary]=None
    judgment_degradation: Optional[Four_Classes]=None
    sense_degradation: Optional[Four_Classes]=None
    lactation: Optional[Three_Classes]=None
    swallowing: Optional[Four_Classes]=None
    muscle: Optional[Four_Classes]=None
    

    

    





