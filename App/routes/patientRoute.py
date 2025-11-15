from fastapi import APIRouter, HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from ..models.UserModel import User
from ..services.PatientServices import PatientServices
from ..services.DoctorServices import DoctorServices
from ..services.UserServices import UserServices
from ..schemas.UserSchemas import UserCreate
from ..schemas.PatientSchemas import PatientCreate,PatientBase,PatientOut
from ..schemas.GeneralSymptomsSchemas import GeneralSymptomsBase,GeneralSymptomsCreate
from ..schemas.SpecificSymptomsSchemas import SpecificSymptomsCreate,SpecificSymptomsBase
from ..schemas.RadioImageSchemas import RadioImageCreate,RadioImageBase
from ..schemas.common import LatestSymptoms,AllSymptoms
from ..dependancies.auth import only_admins,only_patients
from ..schemas.common import NewPatient
from ..schemas.types import Role



from uuid import UUID
from ..dependancies.common import db_dependency


router = APIRouter()
user_services=UserServices()
patient_services=PatientServices()
doctor_services = DoctorServices()



@router.post("/",response_model=PatientBase,dependencies=[only_admins])
async def create_patient(data: NewPatient, session: db_dependency):
    try:
        
        user = await user_services.get_by_phone_number(data.phone_number,session)
        if user is not None :
            raise HTTPException(detail='User is already exist.',status_code=status.HTTP_400_BAD_REQUEST)
        
        user = await user_services.add(UserCreate(phone_number=data.phone_number,password=data.phone_number,role=Role.PATIENT),session)
        if not user :
            raise HTTPException(detail='Inable to create the user.',status_code=status.HTTP_400_BAD_REQUEST)
        
        patient= await patient_services.add(PatientCreate(**data.patient_info.model_dump(),user_id=user.id),session)
        await session.commit()
        return patient

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me",response_model=PatientOut)
async def me(session:db_dependency,current_user=only_patients):
    patient =await patient_services.get_by_user_id(current_user.id,session)
    return patient

@router.get("/get-all-symptoms",response_model=AllSymptoms)
async def get_all_symtoms_(session:db_dependency,current_user:User=only_patients):
    patient = await patient_services.get_by_user_id(str(current_user.id),session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    all_symtons=await patient_services.get_all_symptoms(patient.id,session)
    
    return all_symtons 



@router.get("/{patient_id}",response_model=PatientOut)
async def get_patient(patient_id:UUID,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    return PatientOut(**patient.model_dump())




@router.post("/{patient_id}/add-general-symptoms",response_model=GeneralSymptomsBase,dependencies=[only_admins])
async def add_general_symp(patient_id:UUID,data:GeneralSymptomsBase,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    gs= await patient_services.add_general_symptoms(GeneralSymptomsCreate(**data.model_dump(),patient_id=patient.id),session)
    await session.commit()
    return gs




@router.post("/{patient_id}/add-specific-symptoms",response_model=SpecificSymptomsBase,dependencies=[only_admins])
async def add_specific_symp(patient_id:UUID,data:SpecificSymptomsBase,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    ss= await patient_services.add_specific_symptoms(SpecificSymptomsCreate(**(data.model_dump()),patient_id=patient.id),session)
    await session.commit()
    return ss

@router.post("/{patient_id}/add-radioimage-symptoms",response_model=RadioImageBase,dependencies=[only_admins])
async def add_radio_image(patient_id:UUID,data:RadioImageBase,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    rd= await patient_services.add_radio_image(RadioImageCreate(**data.model_dump(),patient_id=patient.id),session)
    await session.commit()
    return rd

@router.post("/{patient_id}/associate-to/{doctor_id}",response_model=PatientBase,dependencies=[only_admins])
async def associate(patient_id:UUID,doctor_id:UUID,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    doctor =await doctor_services.get(doctor_id,session)
    if not doctor :
        raise HTTPException(detail='Doctor is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    patient = await patient_services.associate_to_doctor(patient,doctor_id,session)
    await session.commit()
    return patient









