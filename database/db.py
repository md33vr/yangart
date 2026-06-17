from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(url=settings.DATABASE_URL,
                                   echo=True,
                                   connect_args={"ssl": None})
session_factory = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass
