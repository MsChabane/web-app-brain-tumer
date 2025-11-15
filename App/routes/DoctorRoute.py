from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from App.models.DoctorModel import Doctor
from ..models.UserModel import User
from ..models.PatientModel import Patient
from ..services.DoctorServices import DoctorServices
from ..services.UserServices import UserServices
from ..services.PatientServices import PatientServices
from ..schemas.UserSchemas import UserCreate
from ..schemas.DoctorSchemas import DoctorCreate
from ..schemas.common import NewDoctor
from ..schemas.types import Role
from ..schemas.PatientSchemas import PatientUpdateStatus,PatientOut
from uuid import UUID
from ..dependancies.common import db_dependency
from typing import Optional,List
from ..dependancies.auth import only_admins,only_doctors
from ..schemas.types import Binary,Four_Classes,FinalStateEnum


router = APIRouter()
user_services=UserServices()
doctor_services=DoctorServices()
patient_services=PatientServices()

@router.post("/new_doctor",dependencies=[only_admins],response_model=Doctor)
async def create_doctor(data: NewDoctor, session: db_dependency):
        if await user_services.check_user_exist(data.user.phone_number,session):
            raise HTTPException(detail='User is already exist.',status_code=400)
        user =user_services.add(user_data=UserCreate(**data.user.model_dump(),role=Role.DOCTOR),session=session)
        
        doctor =doctor_services.add(doctor_data=DoctorCreate(**data.doctor.model_dump(),user_id=user.id),session=session)
        await session.commit()

        return doctor

    
    
@router.get("/",response_model=List[Doctor],dependencies=[only_admins])
async def get_all_doctors(session:db_dependency,page:Optional[int]=1,limit:Optional[int]=10):
    doctors= await doctor_services.get_all(session=session,page=page,limit=limit)
    return doctors



@router.get('/me',dependencies=[only_doctors],response_model=Doctor)
async def get_doctor_info(session:db_dependency,current_user:User=only_doctors):
    doctor =await doctor_services.get_by_user_id(current_user.id,session)
    return doctor

@router.get("/get_patients",response_model=List[PatientOut])
async def get_patient_for_doctor(session:db_dependency,user:User=only_doctors):
    doctor = await doctor_services.get_by_user_id(user.id,session)
    if not doctor:
        raise HTTPException(detail='Doctor is not found.',status_code=status.HTTP_404_NOT_FOUND)
    patients = await patient_services.get_all_for_doctor(doctor.id,session)
    return patients




@router.get("/{id}",response_model=Doctor)
async def get_one(id:UUID,session:db_dependency):
    doctor = await doctor_services.get_with_patients(id,session)
    return doctor 



@router.post("/check/{patient_id}",response_model=Patient )
async def check(patient_id:UUID,session:db_dependency,current_user:User=only_doctors) :
    
    patient =await patient_services.get(patient_id,session)
    if not patient :
        raise HTTPException(detail='Patient is not found.',status_code=status.HTTP_404_NOT_FOUND)
    doctor =await doctor_services.get_by_user_id(current_user.id,session)
    
    if patient.doctor_id !=doctor.id  :
        raise HTTPException (detail="Not allow to check.",status_code=400)
    lts_info = await patient_services.get_latest_infos(patient_id,session)
    if  doctor_services.to_check(patient,latest_symptoms=lts_info):
        patient = await patient_services.update_status(patient,\
            PatientUpdateStatus(tumor_status=Binary.ONE,hospitalisation=Four_Classes.TWO,final_state=FinalStateEnum.T),
            session)
    return patient



@router.delete("/{id}",status_code=status.HTTP_200_OK,dependencies=[only_admins])
async def delete_doctor(id:UUID,session:db_dependency):
        doctor = await doctor_services.get(doctor_id=id,session=session)
        print(doctor)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        user = await user_services.get(doctor.user_id,session)
        
        await doctor_services.detete(doctor,session) 
        await user_services.delete(user,session)
        await session.commit()
        return {"status":'deleted'}
    
    



        



