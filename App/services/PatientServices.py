from sqlmodel import select,SQLModel
from ..db.db import AsyncSession
import  asyncio
from ..models.PatientModel import Patient
from ..models.GeneralSymptomsModel import GeneralSymptoms
from ..models.SpecificSymptomsModel import SpecificSymptoms
from ..models.RadioImageModel import RadioImage
from pydantic import BaseModel

from ..schemas.PatientSchemas import PatientCreate,PatientUpdateStatus,PatientUpdate
from ..schemas.GeneralSymptomsSchemas import GeneralSymptomsCreate,GeneralSymptomsBase
from ..schemas.SpecificSymptomsSchemas import SpecificSymptomsCreate,SpecificSymptomsBase
from ..schemas.RadioImageSchemas import RadioImageCreate,RadioImageBase
from ..schemas.common import LatestSymptoms,AllSymptoms



class PatientServices():
    
    async def add(self,patient_data:PatientCreate,session:AsyncSession):
        patient = Patient(**(patient_data.model_dump()))
        session.add(patient)
        return patient
    
    async def add_general_symptoms(self,general_symptoms_data:GeneralSymptomsCreate,session:AsyncSession):
        gs=GeneralSymptoms(**(general_symptoms_data.model_dump()))
        session.add(gs)
        return gs 
    
    async def add_specific_symptoms(self,specific_symptoms_data:SpecificSymptomsCreate,session:AsyncSession):
        ss=SpecificSymptoms(**(specific_symptoms_data.model_dump()))
        session.add(ss)
        return ss
    async def add_radio_image(self,radio_image:RadioImageCreate,session:AsyncSession):
        rd=RadioImage(**(radio_image.model_dump()))
        session.add(rd)
        return rd
    
    async def get_by_user_id(self,user_id:str,session:AsyncSession):
        statement = select(Patient).where(Patient.user_id == user_id)
        patient = (await session.exec(statement)).first()
        return patient
        
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
        return patient
    
    async def _get_latest(self,Model:SQLModel,patient_id:str,session:AsyncSession):
        stmt = (
            select(Model)
            .where(Model.patient_id == patient_id)
            .order_by(Model.created_at.desc())
            .limit(1)
        )
        return (await session.exec(stmt)).first()
    
    async def _get_latest_general_symptoms(self,patient_id:str,session:AsyncSession):
        return await self._get_latest(GeneralSymptoms,patient_id,session)
    
    async def _get_latest_specific_symptoms(self,patient_id:str,session:AsyncSession):
        return await self._get_latest(SpecificSymptoms,patient_id,session)
    async def _get_latest_radio_image(self,patient_id:str,session:AsyncSession):
        return await self._get_latest(RadioImage,patient_id,session)
    
                    
    async def get_latest_infos(self,patient_id:str,session:AsyncSession):
        gs,ss,rd= await asyncio.gather(
            self._get_latest_general_symptoms(patient_id,session),
            self._get_latest_specific_symptoms(patient_id,session),
            self._get_latest_radio_image(patient_id,session)
        )
        
        return LatestSymptoms(
            general_symptoms=GeneralSymptomsBase(**gs.model_dump()) if gs else None,
    specific_symtoms=SpecificSymptomsBase(**ss.model_dump()) if ss else None,
    radio_image=RadioImageBase(**rd.model_dump()) if rd else None
        ) 
    
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=100):
        statement = select(Patient).offset((page-1)*limit).limit(limit)
        result = await session.exec(statement)
        return result.all()
    
    async def get_all_symptoms (self,patient_id:str,session:AsyncSession):
        gen_stmt = select(GeneralSymptoms).where(GeneralSymptoms.patient_id == patient_id)
        general_symptoms = (await session.exec(gen_stmt)).all()
        
        spec_stmt = select(SpecificSymptoms).where(SpecificSymptoms.patient_id == patient_id)
        specific_symptoms = (await session.exec(spec_stmt)).all()
        
        img_stmt = select(RadioImage).where(RadioImage.patient_id == patient_id)
        radio_images = (await session.exec(img_stmt)).all()
        
        return AllSymptoms(
            general_symptoms=general_symptoms,
            specific_symtoms=specific_symptoms,
            radio_images=radio_images
        )
    async def get_all_for_doctor(self,doctor_id:str,session:AsyncSession):
        statement = select(Patient).where(Patient.doctor_id == doctor_id)
        patients = (await session.exec(statement)).all()
        return patients
         
        