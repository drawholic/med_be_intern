from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import databases
from dotenv import load_dotenv
import os

load_dotenv('.env')

DB_USER=os.getenv('PG_USER')
DB_PASS=os.getenv('PG_PASS')
DB_DB=os.getenv('PG_DB')
DB_PORT=os.getenv('PG_PORT')
DB_HOST=os.getenv('PG_HOST')


DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DB}'
   

database = databases.Database(DB_URL)

engine = create_engine(DB_URL, echo=True)

ss = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    s = ss()
    try:
        yield s
    finally:
        s.close()
