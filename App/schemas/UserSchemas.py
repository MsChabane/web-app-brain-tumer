from pydantic import BaseModel,field_validator
import re
from uuid import UUID




class UserBase(BaseModel):
    phone_number:str
    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        pattern = r"^(?:\+213[5-7]\d{8}|0[5-7]\d{8})$"
        if not re.fullmatch(pattern, v):
            raise ValueError(
                "Invalid Algerian phone number. Must start with '+2135/6/7' or '05/06/07' and have correct length."
            )
        return v

class UserLogin(UserBase):
    password:str
    

class UserUpdate(BaseModel):
    password:str
    

class UserCreate(UserLogin):
    role:str

class UserOut(UserBase):
    id:UUID
    role:str



