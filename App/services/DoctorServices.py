from sqlmodel import select
from sqlalchemy.orm import selectinload
from ..db.db import AsyncSession
from ..models.DoctorModel import Doctor
from ..schemas.DoctorSchemas import DoctorCreate,DoctorUpdate
from ..schemas.common import LatestSymptoms
from ..schemas.PatientSchemas import PatientUpdateStatus
from ..models.PatientModel import Patient
from ..schemas.types import Binary,Seizures,FinalStateEnum,Four_Classes


class DoctorServices:
    
    def update(self,doctor:Doctor,doctor_data:DoctorUpdate,session:AsyncSession):
        for k,v in doctor_data.model_dump(exclude_unset=True).items():
            setattr(doctor, k, v)
        session.add(doctor)
        return doctor
    
        
    async def get(self,doctor_id:str,session:AsyncSession)->Doctor:
        doctor = await session.get(Doctor, doctor_id)
        return doctor 
    
    
        
    
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=100):
        statement = select(Doctor).offset((page-1)*limit).limit(limit)
        result = await session.exec(statement)
        return result.all() 
    
    
    def add( self,doctor_data:DoctorCreate,session:AsyncSession):
        doctor =Doctor(**(doctor_data.model_dump()))
        session.add(doctor)
        return doctor 
    
    async def get_by_user_id(self,user_id:str,session:AsyncSession):
        statement = select(Doctor).where(Doctor.user_id == user_id)
        doctor = (await session.exec(statement)).first()
        return doctor
    
    async def detete(self,doctor:Doctor,session:AsyncSession):
        result = await session.exec(select(Patient).where(Patient.doctor_id == doctor.id))
        patients = result.all()
        for patient in patients:
            patient.doctor_id = None  
            session.add(patient)
        await session.delete(doctor)
        
    def to_check(self,patient:Patient,latest_symptoms:LatestSymptoms)->bool:
        if latest_symptoms.general_symptoms is None and latest_symptoms.specific_symtoms is None and  latest_symptoms.radio_image is None :
            return None
        rd=latest_symptoms.radio_image
        gs=latest_symptoms.general_symptoms
        ss=latest_symptoms.specific_symtoms
        
        if patient.age >62 and patient.antecedents > 0 and gs and gs.seizures == 2 and  gs.drowsiness == 1 and rd and rd.type >= 2:
            return PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.TWO,final_state=FinalStateEnum.T) 
        if  ss and gs and ss.pressure >=2 and gs.fatigue == 2 and gs.memory_pb >=2 :
            return PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.ONE,final_state=FinalStateEnum.D)
        if ss and gs and ss.balance_loss ==1 and  ss.muscle >=2 and patient.age >50:
            return PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.TWO,final_state=FinalStateEnum.T)
        if ss and gs  and ss.judgment_degradation >=2 and ss.sense_degradation >= 2 and gs.seizures==Seizures.TC :
            return PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.TWO,final_state=FinalStateEnum.T)
        if gs and rd and gs.seizures ==Seizures.M and gs.fatigue <=1 and rd.type== 0 :
            return PatientUpdateStatus(tumor_status=Binary.ZERO,hospitalisation=Four_Classes.ZERO,final_state=FinalStateEnum.N)
        if gs and gs.drowsiness == 2 and ss and ss.pressure >=2 and patient.gender > 55:
            return PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.TWO,final_state=FinalStateEnum.T)
        if gs and gs.fatigue == 2 and gs.memory_pb >= 1 and gs.seizures in [Seizures.TC, Seizures.S]:
            return PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.ONE,final_state=FinalStateEnum.D)
        if gs and ss and ss.muscle >=2 and ss.swallowing >=2 and rd and rd.type >=2:
            return PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.THREE,final_state=FinalStateEnum.R)
        return None




