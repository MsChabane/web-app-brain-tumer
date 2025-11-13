from pydantic import BaseModel
from .DoctorSchemas import DoctorBase
from enum import Enum

class NewDoctor(BaseModel):
    doctor:DoctorBase
    phone_number:str

class Role(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"

class FinalStateEnum(str, Enum):
    T = "T"
    D = "D"
    R = "R"
    N = "N"
    
class Gender(str,Enum):
    M='M'
    F='F'

class Binary(int,Enum):
    ZERO = 0
    ONE = 1

class Three_Classes(int,Enum):
    ZERO = 0
    ONE = 1
    TWO = 2

class Four_Classes(int,Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    
    
class Seizures(str,Enum):
    M='M'
    TC="TC"
    S="S"
    C='C'
    
