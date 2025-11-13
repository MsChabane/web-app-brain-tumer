from fastapi.security import HTTPBearer
from fastapi import HTTPException,Depends,Request
from ..utils import decode_token
from typing import Annotated

class AccessTokenChecker(HTTPBearer):
    def __init__(self ):
        super().__init__( auto_error=False)
        
        
    async def __call__(self, request:Request):
        creds = await super().__call__(request)
        
        if creds == None :
            raise HTTPException(detail="no access token provided",status_code=403)
        
          
        token = creds.credentials
        token_data= decode_token(token)
        if token_data is None:
            raise HTTPException(detail="invalid token.",status_code=403)
    
        return token_data





acees_token_checker = Annotated[dict,Depends(AccessTokenChecker())]






