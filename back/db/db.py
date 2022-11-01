
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import databases
from dotenv import load_dotenv
import os

load_dotenv('.env')

DB_USER = os.getenv('PG_USER')
DB_PASS = os.getenv('PG_PASS')
DB_DB = os.getenv('PG_DB')
DB_PORT = os.getenv('PG_PORT')
DB_HOST = os.getenv('PG_HOST')


DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DB}'
   

database = databases.Database(DB_URL)

engine = create_async_engine(DB_URL, echo=True)
 
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session