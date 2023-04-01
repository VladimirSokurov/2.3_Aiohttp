from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''
DB_PORT = ''

engine = create_async_engine('postgresql+asyncpg://DB_USER:DB_PASSWORD@127.0.0.1:DB_PORT/DB_NAME)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Advert(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    user_name = Column(String, nullable=False)
