from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import databases

DB_URL = 'postgresql://postgres:postgres@db:5432/postgres'

database = databases.Database(DB_URL)

engine = create_engine(DB_URL, echo=True)
Base = declarative_base()



Base.metadata.create_all(engine)



