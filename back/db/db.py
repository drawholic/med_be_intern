from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


DB_URL = 'postgresql://postgres:postgres@/be-int/postgres'

engine = sqlalchemy.create_engine(DB_URL)

Base = declarative_base()



Base.metadata.create_all(bind=engine)
