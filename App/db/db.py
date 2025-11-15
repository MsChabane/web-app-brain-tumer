from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import  async_sessionmaker,create_async_engine
from App.settings import setting



engine = create_async_engine(setting.DATABASE_URL,execution_options={"prepared_statement_cache_size": 0})
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)




async def init_db():
    async with engine.begin() as conn:
        from App.models.PatientModel import Patient
        from App.models.UserModel import User
        from App.models.DoctorModel import Doctor
        from App.models.GeneralSymptomsModel import GeneralSymptoms
        from App.models.RadioImageModel import RadioImage
        from App.models.SpecificSymptomsModel import SpecificSymptoms
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession: # type:ignore
    async with async_session() as session:
        yield session


