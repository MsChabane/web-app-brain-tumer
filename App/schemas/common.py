from pydantic import BaseModel
from .DoctorSchemas import DoctorBase
from typing import List
from .PatientSchemas import PatientBase
from .GeneralSymptomsSchemas import GeneralSymptomsBase
from .SpecificSymptomsSchemas import SpecificSymptomsBase
from .RadioImageSchemas import RadioImageBase


class NewDoctor(BaseModel):
    doctor:DoctorBase
    phone_number:str
    
    
class NewPatient(BaseModel):
    phone_number:str
    patient_info: PatientBase
    
class LatestSymptoms(BaseModel):
    
    general_symptoms:GeneralSymptomsBase
    specific_symtoms:SpecificSymptomsBase
    radio_image:RadioImageBase
    

class AllSymptoms(BaseModel):
    general_symptoms:List[GeneralSymptomsBase]
    specific_symtoms:List[SpecificSymptomsBase]
    radio_images:List[RadioImageBase]
