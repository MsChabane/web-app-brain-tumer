from pydantic import BaseModel,ConfigDict
from .DoctorSchemas import DoctorBase
from typing import List,TypeVar,Generic,Optional
from .PatientSchemas import PatientBase
from .GeneralSymptomsSchemas import GeneralSymptomsOut
from .SpecificSymptomsSchemas import SpecificSymptomsOut
from .RadioImageSchemas import RadioImageOut
from .UserSchemas import UserBase


class NewDoctor(BaseModel):
    doctor:DoctorBase
    user:UserBase
    
    
class NewPatient(BaseModel):
    user:UserBase
    patient: PatientBase
    
class LatestSymptoms(BaseModel):
    
    general_symptoms:GeneralSymptomsOut |None
    specific_symtoms:SpecificSymptomsOut |None
    radio_image:RadioImageOut |None
    

class AllSymptoms(BaseModel):
    general_symptoms:List[GeneralSymptomsOut]
    specific_symtoms:List[SpecificSymptomsOut]
    radio_images:List[RadioImageOut]
    model_config = ConfigDict(from_attributes=True)



T = TypeVar("T")
class Message(BaseModel, Generic[T]):
    message: str
    data: Optional[T]=None
    
class Total_insights(BaseModel):
    total_users:int
    total_patients:int
    total_doctors:int
    
