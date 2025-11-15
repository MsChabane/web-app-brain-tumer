from fastapi.security import HTTPBearer
from fastapi import HTTPException,Depends,Request,status
from ..utils import decode_token
from typing import Annotated
from .common import db_dependency
from ..services.UserServices import UserServices
from ..models.UserModel import User
from ..schemas.types import Role
from ..schemas.authSchemas import Token_Data



class AccessTokenChecker(HTTPBearer):
    def __init__(self ):
        super().__init__( auto_error=False)
        
        
    async def __call__(self, request:Request):
        creds = await super().__call__(request)
        
        if creds == None :
            raise HTTPException(detail="No access token provided",status_code=status.HTTP_401_UNAUTHORIZED)
        
          
        token = creds.credentials
        token_data= decode_token(token)
        if token_data is None:
            raise HTTPException(detail="Invalid token.",status_code=status.HTTP_401_UNAUTHORIZED)
    
        return token_data




acees_token_checker = Annotated[Token_Data,Depends(AccessTokenChecker())]


async def get_current_user(token_data:acees_token_checker,session:db_dependency)->User:
    
        user = await UserServices().get(token_data.user_id,session)
        if not user :
            raise HTTPException(detail='user not found',status_code=404)
        return user

current_user=Depends(get_current_user)

def role_required(required_role: str)->User:
    def wrapper(user=current_user):
        if user.role != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return user
    return wrapper

only_admins=Depends(role_required(Role.ADMIN))
only_doctors=Depends(role_required(Role.DOCTOR))
only_patients =Depends(role_required(Role.PATIENT))


