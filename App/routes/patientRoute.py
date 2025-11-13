from fastapi import APIRouter, HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from ..services.PatientServices import PatientServices
from ..services.UserServices import UserServices
from ..schemas.UserSchemas import UserCreate
from ..schemas.PatientSchemas import PatientCreate
from ..schemas.GeneralSymptomsSchemas import GeneralSymptomsBaseCreate
from ..schemas.SpecificSymptomsSchemas import SpecificSymptomsCreate
from ..schemas.RadioImageSchemas import RadioImageCreate
from ..schemas.common import NewPatient
from ..schemas.types import Role
from uuid import UUID
from ..dependancies.common import db_dependency
from typing import Optional,List

router = APIRouter()
user_services=UserServices()
patient_services=PatientServices()



@router.post("/")
async def create_patient(data: NewPatient, session: db_dependency):
    try:
        
        user = await user_services.get_by_phone_number(data.phone_number,session)
        if user is not None and user.role !=Role.PATIENT:
            raise HTTPException(detail='the user is already exist.',status_code=status.HTTP_400_BAD_REQUEST)
        if user is None  :
            user =await user_services.add(user_data=UserCreate(phone_number=data.phone_number,password=data.phone_number,role=Role.PATIENT),session=session)
        
        
        patient= await patient_services.add(PatientCreate(**data.patient_info.model_dump(),user_id=user.id),session)
        await session.flush()
        gs = await patient_services.add_general_symptoms(GeneralSymptomsBaseCreate(**data.general_sympotoms.model_dump(),patient_id=patient.id),session)
        ss = await patient_services.add_specific_symptoms(SpecificSymptomsCreate(**data.specific_symptoms.model_dump(),patient_id=patient.id),session)
        await session.commit()
        return {'patient':patient.model_dump(),
                "gs":gs.model_dump(),'ss':ss.model_dump()
                }

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{patient_id}")
async def get_one(patient_id:UUID,session:db_dependency):
    patient = await patient_services.get_infos(patient_id,session)
    print(patient)
    return ""



