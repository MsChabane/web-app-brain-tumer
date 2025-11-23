from pydantic import BaseModel,ConfigDict
from uuid import UUID
from .types import Three_Classes,Seizures
from typing import Optional 
from datetime import datetime

class GeneralSymptomsBase(BaseModel):
    headaches:Three_Classes
    seizures:Seizures 
    fatigue: Three_Classes
    drowsiness: Three_Classes
    sleep_pb: Three_Classes
    memory_pb: Three_Classes
   
    


    
class GeneralSymptomsCreate(GeneralSymptomsBase):
    patient_id:UUID
    
class GeneralSymptomsOut(GeneralSymptomsBase):
    id:UUID
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)

class GeneralSymptomsUpdate(BaseModel):
    headaches:Optional[Three_Classes]=None
    seizures:Optional[Seizures] =None
    fatigue: Optional[Three_Classes]=None
    drowsiness: Optional[Three_Classes]=None
    sleep_pb: Optional[Three_Classes]=None
    memory_pb: Optional[Three_Classes]=None
    
    

    

    

    





