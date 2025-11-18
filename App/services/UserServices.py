from sqlmodel import select
from ..db.db import AsyncSession
from ..models.UserModel import User
from ..schemas.UserSchemas import UserCreate,UserUpdate
from ..utils import hash


class UserServices:
    async def change_password(self,user:User,new_password:str,session:AsyncSession):
        user.password= hash(new_password)
        session.add(user)
        return user
        
    async def get(self,user_id:str,session:AsyncSession):
        user = await session.get(User, user_id)
        return user 
    
    
    async def get_by_phone_number(self,phone_number:str,session:AsyncSession):
        statement = select(User).where(User.phone_number == phone_number)
        user = (await session.exec(statement)).first()
        return user
    
      
    async def check_user_exist(self,phone_number:str,session:AsyncSession):
        return (await self.get_by_phone_number(phone_number,session)) is not None
    
    def add( self,user_data:UserCreate,session:AsyncSession):
        user_data.password=hash(user_data.password)
        user =User(**(user_data.model_dump()))
        session.add(user)
        return user     

    async def delete(self,user:User,session:AsyncSession):
        await session.delete(user)
        
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=100):
        statement = select(User).offset((page-1)*limit).limit(limit)
        result = await session.exec(statement)
        return result.all()

