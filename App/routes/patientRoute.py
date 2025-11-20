from fastapi import APIRouter, HTTPException,status
from ..services.PatientServices import PatientServices
from ..services.DoctorServices import DoctorServices
from ..services.UserServices import UserServices
from ..schemas.UserSchemas import UserCreate
from ..schemas.PatientSchemas import PatientCreate,PatientOut,PatientUpdate
from ..schemas.GeneralSymptomsSchemas import GeneralSymptomsBase,GeneralSymptomsCreate,GeneralSymptomsOut,GeneralSymptomsUpdate
from ..schemas.SpecificSymptomsSchemas import SpecificSymptomsCreate,SpecificSymptomsBase,SpecificSymptomsOut,SpecificSymptomsUpdate
from ..schemas.RadioImageSchemas import RadioImageCreate,RadioImageBase,RadioImageOut
from ..schemas.common import AllSymptoms,Message,NewPatient,LatestSymptoms
from ..dependancies.auth import only_admins,only_patients
from ..schemas.types import Role
from typing import List ,Optional
from uuid import UUID
from ..dependancies.common import db_dependency

router = APIRouter()
user_services=UserServices()
patient_services=PatientServices()
doctor_services = DoctorServices()



@router.post("/new-patient",response_model=PatientOut,dependencies=[only_admins])
async def create_patient(data: NewPatient, session: db_dependency):

    user = await user_services.get_by_phone_number(data.user.phone_number,session)
    if user is not None :
        raise HTTPException(detail='User is already exist.',status_code=status.HTTP_400_BAD_REQUEST)
    
    user =  user_services.add(UserCreate(**data.user.model_dump(),password=data.user.phone_number,role=Role.PATIENT),session)

    
    patient= await patient_services.add(PatientCreate(**data.patient.model_dump(),user_id=user.id),session)
    await session.commit()
    return patient

@router.get("/all",response_model=List[PatientOut],dependencies=[only_admins])
async def get_all_patients(session:db_dependency,page:Optional[int]=1,limit:Optional[int]=10):
    patients= await patient_services.get_all(session=session,page=page,limit=limit)
    print(patients)
    return patients  

@router.get("/me",response_model=PatientOut)
async def me(session:db_dependency,current_user=only_patients):
    patient =await patient_services.get_by_user_id(current_user.id,session)
    print(patient)
    return patient

@router.get("/get-latest-symptoms",response_model=LatestSymptoms)
async def get_latest_symtoms_(session:db_dependency,current_user=only_patients):
    patient = await patient_services.get_by_user_id(str(current_user.id),session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    latest_symp=await patient_services.get_latest_infos(patient.id,session)
    
    return latest_symp 

@router.get("/no-associated",response_model=List[PatientOut])
async def get_no_associated(session:db_dependency):
    return await patient_services.get_no_associated_patients(session)
    

@router.get("{patient_id}/get-all-symptoms",response_model=AllSymptoms,dependencies=[only_admins])
async def get_all_symtoms_(patient_id:UUID,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    all_symtons=await patient_services.get_all_symptoms(patient.id,session)
    
    return all_symtons


@router.get("/{patient_id}",response_model=PatientOut)
async def get_patient(patient_id:UUID,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    return patient




@router.post("/{patient_id}/add-general-symptoms",response_model=GeneralSymptomsOut,dependencies=[only_admins])
async def add_general_symp(patient_id:UUID,data:GeneralSymptomsBase,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    gs= await patient_services.add_general_symptoms(GeneralSymptomsCreate(**data.model_dump(),patient_id=patient.id),session)
    await session.commit()
    return gs


@router.post("/{patient_id}/add-specific-symptoms",response_model=SpecificSymptomsOut,dependencies=[only_admins])
async def add_specific_symp(patient_id:UUID,data:SpecificSymptomsBase,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    ss= await patient_services.add_specific_symptoms(SpecificSymptomsCreate(**(data.model_dump()),patient_id=patient.id),session)
    await session.commit()
    return ss

@router.post("/{patient_id}/add-radioimage-symptoms",response_model=RadioImageOut,dependencies=[only_admins])
async def add_radio_image(patient_id:UUID,data:RadioImageBase,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    rd= await patient_services.add_radio_image(RadioImageCreate(**data.model_dump(),patient_id=patient.id),session)
    await session.commit()
    return rd


@router.post("/{patient_id}/associate-to/{doctor_id}",response_model=PatientOut,dependencies=[only_admins])
async def associate(patient_id:UUID,doctor_id:UUID,session:db_dependency):
    patient = await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    doctor =await doctor_services.get(doctor_id,session)
    if not doctor :
        raise HTTPException(detail='Doctor is not exist.',status_code=status.HTTP_404_NOT_FOUND)
    patient = await patient_services.associate_to_doctor(patient,doctor_id,session)
    await session.commit()
    await session.refresh(patient)
    return patient

@router.put("/{id}",response_model=PatientOut)
async def update(id:UUID,data:PatientUpdate,session:db_dependency):
    patient = await patient_services.get(id,session)
    if not patient :
        raise HTTPException(detail='Patient is not Found',status_code=404)
    patient = patient_services.update(patient ,data,session)
    await session.commit()
    return patient 

@router.put("/general-symptoms/{id}",response_model=GeneralSymptomsOut)
async def update(id:UUID,data:GeneralSymptomsUpdate,session:db_dependency):
    gs = await patient_services.get_general_symptom(id,session)
    if not gs :
        raise HTTPException(detail='General symptoms is not Found',status_code=404)
    gs = patient_services.update_general_symptoms(gs ,data,session)
    await session.commit()
    return gs 

@router.put("/specific-symptoms/{id}",response_model=SpecificSymptomsOut)
async def update(id:UUID,data:SpecificSymptomsUpdate,session:db_dependency):
    ss = await patient_services.get_specific_symptom(id,session)
    if not ss :
        raise HTTPException(detail='Specific symptoms is not Found',status_code=404)
    ss = patient_services.update_specific_symptoms(ss ,data,session)
    await session.commit()
    return ss 

@router.put("/radio-image/{id}",response_model=RadioImageOut)
async def update(id:UUID,data:RadioImageBase,session:db_dependency):
    rd = await patient_services.get_radio_image(id,session)
    if not rd :
        raise HTTPException(detail='Radio-image is not Found',status_code=404)
    rd = patient_services.update_radio_image(rd ,data,session)
    await session.commit()
    return rd 

@router.delete("/{id}",status_code=status.HTTP_200_OK,response_model=Message[None],dependencies=[])
async def delete_patient(id:UUID,session:db_dependency):
        patient = await patient_services.get(id,session)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        user = await user_services.get(patient.user_id,session)
        
        await patient_services.delete(patient,session) 
        await user_services.delete(user,session)
        await session.commit()
        return Message(message="deleted")