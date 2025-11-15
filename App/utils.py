import bcrypt
from jose import jwt
from datetime import datetime,timedelta,timezone
from .schemas.authSchemas import Token_Data

from .settings import setting

def hash(password:str)-> str:
    salt = bcrypt.gensalt()
    hashed=bcrypt.hashpw(password=password.encode(),salt=salt)
    return hashed.decode()

def checkpwd(password:str,hashed:str)-> bool:
    return bcrypt.checkpw(password.encode(),hashed.encode())


def create_token(data:Token_Data):
    expiry = timedelta(minutes=20) 
    dt=data.model_dump()
    dt["exp"]=int((datetime.now(timezone.utc)+expiry).timestamp())
    token = jwt.encode(dt,setting.JWT_SECRET)
    return token

def decode_token(token:str)->Token_Data|None:
    try:
        token_data= jwt.decode(token,setting.JWT_SECRET,algorithms=['HS256'])
        return Token_Data(user_id=token_data['user_id'])
    except Exception as e:
        return None