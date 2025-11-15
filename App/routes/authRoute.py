from fastapi import APIRouter,HTTPException,status

from ..dependancies.common import db_dependency
from ..dependancies.auth import current_user
from ..schemas.UserSchemas import UserLogin,UserBase,UserCreate,UserOut
from ..services.UserServices import UserServices
from ..schemas.authSchemas import Token_Data,Token
from ..schemas.types import Role


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
    
@router.post("/create-admin",status_code=201)
async def signup_admins(data:UserBase,session:db_dependency) :
    if  await user_services.check_user_exist(data.phone_number,session):
        raise HTTPException(
            detail='user is already exist',status_code=400
        )
    
    user=await user_services.add(UserCreate(**data.model_dump(),role=Role.ADMIN),session)
    await session.commit()
    return ""


@router.post("/profile",status_code=200,response_model=UserOut)
async def profile(user=current_user) :
    return UserOut(**user.model_dump())
    


    
    
    
    



