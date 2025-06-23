from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

db = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(db)


async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
