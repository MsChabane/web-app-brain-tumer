from pydantic import BaseModel
from .DoctorSchemas import DoctorBase
from enum import Enum
from .PatientSchemas import PatientBase
from .GeneralSymptomsSchemas import GeneralSymptomsBase
from .SpecificSymptomsSchemas import SpecificSymptomsBase

class NewDoctor(BaseModel):
    doctor:DoctorBase
    phone_number:str
    
class NewPatient(BaseModel):
    phone_number:str
    patient_info: PatientBase
    general_sympotoms:GeneralSymptomsBase
    specific_symptoms:SpecificSymptomsBase



