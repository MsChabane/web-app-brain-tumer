from pydantic import BaseModel
from uuid import UUID
from .types import Three_Classes,Four_Classes,Binary

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

    
    
    

    

    





