from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from App.models.DoctorModel import Doctor
from ..services.DoctorServices import DoctorServices
from ..services.UserServices import UserServices
from ..schemas.UserSchemas import UserCreate
from ..schemas.DoctorSchemas import DoctorCreate
from ..schemas.common import NewDoctor,Role
from uuid import UUID
from ..dependancies.common import db_dependency
from typing import Optional,List



router = APIRouter()
user_services=UserServices()
doctor_services=DoctorServices()


@router.post("/")
async def create_doctor(data: NewDoctor, session: db_dependency):
    try:
        print(data.doctor)
        if await user_services.check_user_exist(data.phone_number,session):
            return HTTPException(detail='doctor is already exist.',status_code=400)
        user =await user_services.add(user_data=UserCreate(phone_number=data.phone_number,password=data.phone_number,role=Role.DOCTOR),session=session)
        
        doctor =await doctor_services.add(doctor_data=DoctorCreate(**data.doctor.model_dump(),user_id=user.id),session=session)
        await session.commit()

        return {"doctor":doctor.model_dump(),'user':user.model_dump()}

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/",response_model=List[Doctor])
async def get_all_doctors(session:db_dependency,page:Optional[int]=1,limit:Optional[int]=10):
    doctors= await doctor_services.get_all(session=session,page=page,limit=limit)
    return doctors
    
@router.get("/{id}",response_model=Doctor)
async def get_one(id:UUID,session:db_dependency):
    doctor = await doctor_services.get_with_patients(id,session)
    return doctor 
     

    
@router.delete("/{id}",status_code=status.HTTP_200_OK)
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


        



