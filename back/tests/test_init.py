import pytest
from db.models import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from core import app
from dotenv import load_dotenv
import os
import pytest_asyncio

load_dotenv('.env')


DB_USER = os.getenv('PG_USER_TEST')
DB_PASS = os.getenv('PG_PASS_TEST')
DB_DB = os.getenv('PG_DB_TEST')
DB_PORT = os.getenv('PG_PORT_TEST')
DB_HOST = os.getenv('PG_HOST_TEST')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@172.29.0.3:{DB_PORT}/{DB_DB}'

engine = create_async_engine(DB_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def get_db() -> AsyncSession:
    # await init_models()
    async with async_session() as session:
        yield session


client = TestClient(app)
