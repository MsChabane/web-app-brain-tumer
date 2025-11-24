from fastapi import APIRouter,HTTPException,status
from ..dependancies.common import db_dependency
from ..dependancies.auth import current_user,only_admins
from ..schemas.UserSchemas import UserLogin,UserBase,UserCreate,UserOut,UserUpdate
from ..services.UserServices import UserServices
from ..schemas.authSchemas import Token_Data,Token
from ..schemas.types import Role
from ..schemas.common import Message
from typing import List ,Optional
from uuid import UUID

from ..utils import create_token,checkpwd


router =APIRouter()
user_services=UserServices()


@router.post("/login",response_model=Token)
async def login(data:UserLogin,session:db_dependency):
    user = await user_services.get_by_phone_number(data.phone_number,session)
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User is not found.")
    if not checkpwd(data.password,user.password) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid Credentials.')
    
    token = create_token(data=Token_Data(user_id=str(user.id)))
    return Token(
        access_token=token,role=user.role,
    )

    
@router.post("/create-admin",status_code=201,dependencies=[only_admins],response_model=UserOut)
async def signup_admins(data:UserBase,session:db_dependency) :
    if  await user_services.check_user_exist(data.phone_number,session):
        raise HTTPException(
            detail='User is already exist',status_code=400
        )
    
    user= user_services.add(UserCreate(**data.model_dump(),password=data.phone_number,role=Role.ADMIN),session)
    await session.commit()
    return user

@router.get("/users/all",response_model=List[UserOut],dependencies=[only_admins])
async def get_all_users(session:db_dependency,page:Optional[int]=1,limit:Optional[int]=10):
    users= await user_services.get_all(session=session,page=page,limit=limit)
    return users  

@router.get("/profile",status_code=200,response_model=UserOut)
async def profile(user=current_user) :
    return user

@router.post("/user/change-password",response_model=Message[None])
async def change_password(data:UserUpdate,session:db_dependency,user=current_user):
    user=await user_services.change_password(user,data.password,session)
    await session.commit()
    return Message(message='Password Changed')

@router.delete("/users/admin/{user_id}",dependencies=[],response_model=Message[None])
async def delete_admin(user_id:UUID,session:db_dependency,current_user=only_admins):
    user =await user_services.get(user_id=user_id,session=session)
    if user is None :
        raise HTTPException(
            detail='User is not found.',status_code=400
        )
    if user.role !=Role.ADMIN:
        raise HTTPException(
            detail='User is not admin.',status_code=400
        )
    if user.id == current_user.id:
        raise HTTPException(
            detail="Can't delete yourself.",status_code=400
        )
    await user_services.delete(user,session)
    await session.commit()
    return Message(message="deleted")
    

    


    
    
    
    



