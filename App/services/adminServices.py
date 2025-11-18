from sqlmodel import func, select,SQLModel
from ..models.DoctorModel import Doctor
from ..models.UserModel import User
from ..models.PatientModel import Patient
from ..db.db import AsyncSession

class AdminServices:
    
    async def _get_totat_for(self,model:SQLModel ,session: AsyncSession)->int:
        result = await session.exec(select(func.count(model.id)))
        return result.one() 
    async def get_total_users(self, session: AsyncSession) -> int:
        return await self._get_totat_for(User,session)

    async def get_total_patients(self, session: AsyncSession) -> int:
        return await self._get_totat_for(Patient,session)

    async def get_total_doctors(self, session: AsyncSession) -> int:
        return await self._get_totat_for(Doctor,session)

    
