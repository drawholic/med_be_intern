from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases

<<<<<<< HEAD
DB_URL = 'postgresql://postgres:postgres@db:5432/postgres'
=======
DB_URL = 'postgresql://postgres:postgres@localhost:5432/postgres'
>>>>>>> 13736ac1e8f9f4ce78e4c570d92b5cb1dde702a1

database = databases.Database(DB_URL)


ss = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_engine(DB_URL, echo=True)
Base = declarative_base()


def get_db():
    s = ss()
    try:
        yield s
    finally:
        s.close()
