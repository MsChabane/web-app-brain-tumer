from sqlmodel import select,SQLModel,delete,desc
from sqlalchemy.orm import selectinload
from ..db.db import AsyncSession
import  asyncio
from ..models.PatientModel import Patient
from ..models.GeneralSymptomsModel import GeneralSymptoms
from ..models.SpecificSymptomsModel import SpecificSymptoms
from ..models.RadioImageModel import RadioImage
from pydantic import BaseModel
from ..schemas.PatientSchemas import PatientCreate,PatientUpdateStatus,PatientUpdate
from ..schemas.GeneralSymptomsSchemas import GeneralSymptomsCreate,GeneralSymptomsBase,GeneralSymptomsUpdate
from ..schemas.SpecificSymptomsSchemas import SpecificSymptomsCreate,SpecificSymptomsBase,SpecificSymptomsUpdate
from ..schemas.RadioImageSchemas import RadioImageCreate,RadioImageBase
from ..schemas.common import LatestSymptoms,AllSymptoms



class PatientServices():
    
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=10)->list[Patient]:
        statement = select(Patient).options(selectinload(Patient.doctor)) .offset((page-1)*limit).limit(limit)
        result = await session.exec(statement)
        return result.all() 
    
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
        statement = select(Patient).where(Patient.user_id == user_id).options(selectinload(Patient.doctor)) 
        patient = (await session.exec(statement)).first()
        return patient
    
    async def _get(self,id:str,model:SQLModel,session:AsyncSession)->SQLModel:
        return await session.get(model,id)
    
    async def get(self ,id:str,session:AsyncSession)->Patient:
        patient = await self._get(id,Patient,session)
        return patient
    
    async def get_radio_image(self ,id:str,session:AsyncSession)->RadioImage:
         return await self._get(id,RadioImage,session)
     
    async def get_general_symptom(self ,id:str,session:AsyncSession)->GeneralSymptoms:
         return await self._get(id,GeneralSymptoms,session)
     
    async def get_specific_symptom(self ,id:str,session:AsyncSession)->SpecificSymptoms:
         return await self._get(id,SpecificSymptoms,session)
        
    
        
    def _update(self ,model:SQLModel,data:BaseModel)->SQLModel:
        for k,v in data.model_dump(exclude_unset=True).items():
            setattr(model,k,v)
        return model
    
    async def update_state(self,patient:Patient,new_state:PatientUpdateStatus,session:AsyncSession):
        patient= self._update(patient,new_state)
        session.add(patient)
        return patient
        
    def update(self,patient:Patient,new_data:PatientUpdate,session:AsyncSession):
        patient= self._update(patient,new_data) 
        session.add(patient)
        return patient
    
    def update_general_symptoms(self,general_symtoms:GeneralSymptoms,data:GeneralSymptomsUpdate,session:AsyncSession):
        general_symtoms= self._update(general_symtoms,data)
        session.add(general_symtoms)
        return general_symtoms
    
    def update_specific_symptoms(self,specific_symtoms:SpecificSymptoms,data:SpecificSymptomsUpdate,session:AsyncSession):
        specific_symtoms= self._update(specific_symtoms,data)
        session.add(specific_symtoms)
        return specific_symtoms
    
    def update_radio_image(self,radioimage:RadioImage,data:RadioImageBase,session:AsyncSession):
        radioimage= self._update(radioimage,data)
        session.add(radioimage)
        return radioimage
    

    async def delete(self,patient:Patient,session:AsyncSession):
        await asyncio.gather(        
            session.exec(delete(GeneralSymptoms).where(GeneralSymptoms.patient_id == patient.id)),
            session.exec(delete(SpecificSymptoms).where(SpecificSymptoms.patient_id == patient.id)),
            session.exec(delete(RadioImage).where(RadioImage.patient_id == patient.id))
        )
        await session.exec(delete(Patient).where(Patient.id == patient.id))
        
        
    
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
    
    async def _get_latest_general_symptoms(self,patient_id:str,session:AsyncSession)->GeneralSymptoms|None:
        return await self._get_latest(GeneralSymptoms,patient_id,session)
    
    async def _get_latest_specific_symptoms(self,patient_id:str,session:AsyncSession)->SpecificSymptoms|None:
        return await self._get_latest(SpecificSymptoms,patient_id,session)
    async def _get_latest_radio_image(self,patient_id:str,session:AsyncSession)->RadioImage|None:
        return await self._get_latest(RadioImage,patient_id,session)
    
                    
    async def get_latest_infos(self,patient_id:str,session:AsyncSession):
        gs,ss,rd= await asyncio.gather(
            self._get_latest_general_symptoms(patient_id,session),
            self._get_latest_specific_symptoms(patient_id,session),
            self._get_latest_radio_image(patient_id,session)
        )
        
        return LatestSymptoms(
            general_symptoms=gs.model_dump() if gs else None,
    specific_symtoms=ss.model_dump() if ss else None,
    radio_image=rd.model_dump()  if rd else None
        ) 
    
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=100):
        statement = select(Patient).offset((page-1)*limit).limit(limit)
        result = await session.exec(statement)
        return result.all()
    
    async def _get_all_general_symp_for(self,patient_id:str,session:AsyncSession):
        gen_stmt = select(GeneralSymptoms).where(GeneralSymptoms.patient_id == patient_id).order_by(desc(GeneralSymptoms.created_at))
        return  (await session.exec(gen_stmt)).all()
    
    async def _get_all_specific_symp_for(self,patient_id:str,session:AsyncSession):
        spec_stmt = select(SpecificSymptoms).where(SpecificSymptoms.patient_id == patient_id).order_by(desc(SpecificSymptoms.created_at))
        return  (await session.exec(spec_stmt)).all()
    
    async def _get_all_radio_images_for(self,patient_id:str,session:AsyncSession):
        img_stmt = select(RadioImage).where(RadioImage.patient_id == patient_id).order_by(desc(RadioImage.created_at))
        return (await session.exec(img_stmt)).all()
    
    
    async def get_all_symptoms (self,patient_id:str,session:AsyncSession):
        general_symptoms,specific_symptoms ,radio_images =  await asyncio.gather(
                         self._get_all_general_symp_for(patient_id,session),
                         self._get_all_specific_symp_for(patient_id,session),
                         self._get_all_radio_images_for(patient_id,session)
        )
        return AllSymptoms(
            general_symptoms=general_symptoms,
            specific_symtoms=specific_symptoms,
            radio_images=radio_images
        )
    async def get_all_for_doctor(self,doctor_id:str,session:AsyncSession):
        statement = select(Patient).where(Patient.doctor_id == doctor_id)
        patients = (await session.exec(statement)).all()
        return patients
    
    
    async def get_no_associated_patients(self, session: AsyncSession):
        stmt = select(Patient).where(Patient.doctor_id == None)
        return (await session.exec(stmt)).all()
         