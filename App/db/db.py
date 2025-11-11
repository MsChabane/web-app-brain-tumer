from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import  async_sessionmaker,create_async_engine
from App.settings import setting



engine = create_async_engine(setting.DATABASE_URL)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)




async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession: # type:ignore
    async with async_session() as session:
        yield session


