from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

async_session = async_sessionmaker(class_=AsyncSession, expire_on_commit=False)
