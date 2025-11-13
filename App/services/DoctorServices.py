from sqlmodel import select
from sqlalchemy.orm import selectinload
from ..db.db import AsyncSession
from ..models.DoctorModel import Doctor
from ..schemas.DoctorSchemas import DoctorCreate,DoctorUpdate

from ..models.PatientModel import Patient



class DoctorServices:
    
    async def update(self,doctor:Doctor,doctor_data:DoctorUpdate,session:AsyncSession):
        for k,v in doctor_data.model_dump(exclude_unset=True).items():
            setattr(doctor, k, v)
        session.add(doctor)
        return doctor
    
        
    async def get(self,doctor_id:str,session:AsyncSession):
        doctor = await session.get(Doctor, doctor_id)
        return doctor 
    async def get_with_patients(self,doctor_id:str,session:AsyncSession):
        doctor =await session.get(Doctor, doctor_id,populate_existing=True)
        return doctor
        
    
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=100):
        statement = select(Doctor).offset((page-1)*limit).limit(limit)
        result = await session.exec(statement)
        return result.all() 
    
    
    async def add( self,doctor_data:DoctorCreate,session:AsyncSession):
        doctor =Doctor(**(doctor_data.model_dump()))
        session.add(doctor)

        return doctor 
    
    async def to_check(self,patient_id):
        pass    

    async def detete(self,doctor:Doctor,session:AsyncSession):
        result = await session.exec(select(Patient).where(Patient.doctor_id == doctor.id))
        patients = result.all()
        for patient in patients:
            patient.doctor_id = None  
            session.add(patient)
        await session.delete(doctor)
        






