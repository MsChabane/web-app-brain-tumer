from pydantic import BaseModel
from .DoctorSchemas import DoctorBase
from typing import List
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
    
    general_symptoms:GeneralSymptomsBase
    specific_symtoms:SpecificSymptomsBase
    radio_image:RadioImageBase
    

class AllSymptoms(BaseModel):
    general_symptoms:List[GeneralSymptomsBase]
    specific_symtoms:List[SpecificSymptomsBase]
    radio_images:List[RadioImageBase]
