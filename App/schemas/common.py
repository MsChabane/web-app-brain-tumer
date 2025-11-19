from pydantic import BaseModel
from pydantic.generics import GenericModel
from .DoctorSchemas import DoctorBase
from typing import List,TypeVar,Generic,Optional
from .PatientSchemas import PatientBase
from .GeneralSymptomsSchemas import GeneralSymptomsBase
from .SpecificSymptomsSchemas import SpecificSymptomsBase
from .RadioImageSchemas import RadioImageBase
from .UserSchemas import UserBase


class NewDoctor(BaseModel):
    doctor:DoctorBase
    user:UserBase
    
    
class NewPatient(BaseModel):
    user:UserBase
    patient: PatientBase
    
class LatestSymptoms(BaseModel):
    
    general_symptoms:GeneralSymptomsBase |None
    specific_symtoms:SpecificSymptomsBase |None
    radio_image:RadioImageBase |None
    

class AllSymptoms(BaseModel):
    general_symptoms:List[GeneralSymptomsBase]
    specific_symtoms:List[SpecificSymptomsBase]
    radio_images:List[RadioImageBase]



T = TypeVar("T")
class Message(GenericModel, Generic[T]):
    message: str
    data: Optional[T]=None
    
class Total_insights(BaseModel):
    total_users:int
    total_patients:int
    total_doctors:int
    
