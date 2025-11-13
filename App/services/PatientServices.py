from sqlmodel import select
from ..db.db import AsyncSession
from ..models.PatientModel import Patient
from ..models.GeneralSymptomsModel import GeneralSymptoms
from ..models.SpecificSymptomsModel import SpecificSymptoms
from pydantic import BaseModel

from ..schemas.PatientSchemas import PatientCreate,PatientUpdateStatus,PatientUpdate
from ..schemas.GeneralSymptomsSchemas import GeneralSymptomsBaseCreate
from ..schemas.SpecificSymptomsSchemas import SpecificSymptomsCreate


class PatientServices():
    async def add(self,patient_data:PatientCreate,session:AsyncSession):
        patient = Patient(**(patient_data.model_dump()))
        session.add(patient)
        return patient
    
    async def add_general_symptoms(self,general_symptoms_data:GeneralSymptomsBaseCreate,session:AsyncSession):
        gs=GeneralSymptoms(**(general_symptoms_data.model_dump()))
        session.add(gs)
        return gs 
    async def add_specific_symptoms(self,specific_symptoms_data:SpecificSymptomsCreate,session:AsyncSession):
        ss=SpecificSymptoms(**(specific_symptoms_data.model_dump()))
        session.add(ss)
        return ss
        
    async def get(self ,id:str,session:AsyncSession):
        patient = await session.get(Patient,id)
        return patient
        
    def _update(self ,patient:Patient,data:BaseModel):
        for k,v in data.model_dump(exclude_unset=True).items():
            setattr(patient,k,v)
        return patient
    async def update_status(self,patient:Patient,status:PatientUpdateStatus,session:AsyncSession):
        patient= self._update(patient,status)
        session.add(patient)
        return patient
        
    async def update(self,patient:Patient,new_data:PatientUpdate,session:AsyncSession):
        patient= self._update(patient,new_data) 
        session.add(patient)
        return patient

    async def delete(self,patient:Patient,session:AsyncSession):
        pass
    
    async  def associate_to_doctor(self,patient:Patient,doctor_id:str,session:AsyncSession):
        patient.doctor_id=doctor_id
        session.add(patient)
    
    async def get_infos(self,patient_id:str,session:AsyncSession):
        patient = await session.get(Patient,patient_id,populate_existing=True)
        return patient