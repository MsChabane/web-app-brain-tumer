from pydantic import BaseModel


class Token(BaseModel):
    access_token:str
    type:str='Bearer'
    role:str

class Token_Data(BaseModel):
    user_id:str

class Change_password(BaseModel):
    password:str

