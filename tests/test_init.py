import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from back.app import app
from dotenv import load_dotenv
import os

load_dotenv('.env')


DB_USER = os.getenv('PG_USER_TEST')
DB_PASS = os.getenv('PG_PASS_TEST')
DB_DB = os.getenv('PG_DB_TEST')
DB_PORT = os.getenv('PG_PORT_TEST')
DB_HOST = os.getenv('PG_HOST_TEST')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DB}'

engine = create_async_engine(DB_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


client = TestClient(app)