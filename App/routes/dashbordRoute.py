from fastapi import APIRouter
from ..dependancies.common import db_dependency
from ..dependancies.auth import only_admins
from ..services.adminServices import AdminServices
from ..schemas.common import Message


router =APIRouter()
admin=AdminServices()

@router.get("/total-dectors",dependencies=[only_admins],response_model=Message[int])
async def total_doctors(session:db_dependency):
    return Message(message="total dotores",data=await admin.get_total_doctors(session))
@router.get("/total-patients",dependencies=[only_admins],response_model=Message[int])
async def total_patients(session:db_dependency):
    return Message(message="total patients",data=await admin.get_total_patients(session))
     

@router.get("/total-users",dependencies=[only_admins],response_model=Message[int])
async def total_users(session:db_dependency):
    return Message(message="total dotores",data=await admin.get_total_users(session))






