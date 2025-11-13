from pydantic import BaseModel

class UserBase(BaseModel):
    phone_number:str
    password:str

class UserLogin(UserBase):
    pass
    

class UserUpdate(BaseModel):
    password:str


class UserCreate(UserBase):
    role:str





