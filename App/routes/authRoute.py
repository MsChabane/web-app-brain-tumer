from fastapi import APIRouter,HTTPException,status
from ..dependancies.common import db_dependency
from ..schemas.UserSchemas import UserLogin
from ..services.UserServices import UserServices

from ..utils import create_token,checkpwd


router =APIRouter()
user_services=UserServices()

@router.post("/")
async def login(data:UserLogin,session:db_dependency):
    user = await user_services.get_by_phone_number(data.phone_number,session)
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User is not found.")
    if not checkpwd(data.password,user.password) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid Credentials.')
    data={
        'user_id':str(user.id),'role':user.role
    }
    token = create_token(data=data)
    return {
        'access_token':token,"type":'Bearer','role':user.role
    }
    
    

    
    
    
    
    



