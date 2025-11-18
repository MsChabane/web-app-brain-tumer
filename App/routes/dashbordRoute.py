from fastapi import APIRouter
import asyncio
from ..dependancies.common import db_dependency
from ..dependancies.auth import only_admins
from ..services.adminServices import AdminServices
from ..schemas.common import Message,Total_insights


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


@router.get("/total",response_model=Message[Total_insights])
async def get_totals(session:db_dependency):
    
    total_u = await admin.get_total_users(session)
    total_d = await admin.get_total_doctors(session)
    total_p = await admin.get_total_patients(session)
    
    return Message(message="total_insights",data=Total_insights(total_doctors=total_d,total_users=total_u,total_patients=total_p))

