import bcrypt
from jose import jwt
from datetime import datetime,timedelta,timezone

from .settings import setting

def hash(password:str)-> str:
    salt = bcrypt.gensalt()
    hashed=bcrypt.hashpw(password=password.encode(),salt=salt)
    return hashed.decode()

def checkpwd(password:str,hashed:str)-> bool:
    return bcrypt.checkpw(password.encode(),hashed.encode())


def create_token(data:dict):
    expiry = timedelta(minutes=20) 
    data["exp"]=int((datetime.now(timezone.utc)+expiry).timestamp())
    token = jwt.encode(data,setting.JWT_SECRET)
    return token

def decode_token(token:str)->dict|None:
    try:
        token_data= jwt.decode(token,setting.JWT_SECRET,algorithms=['HS256'])
        return token_data
    except Exception as e:
        return None