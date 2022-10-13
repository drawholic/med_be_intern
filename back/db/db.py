from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
from dotenv import load_dotenv

load_dotenv()

DB_USER=os.getenv('PG_USER')
DB_PASS=os.getenv('PG_PASS')
DB_DB=os.getenv('PG_DB')


DB_URL = f`postgresql://${DB_USER}:${DB_PASS}@db:5432/${DB_DB}`
   

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
