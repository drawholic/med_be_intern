from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import database, engine
from db.models import Base
import aioredis
from users.router import users
from log import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.include_router(users)

@app.on_event('startup')
async def startup():
    
    logger.info('SERVER STARTED')
    await database.connect()
    redis = await aioredis.from_url('redis://localhost')
    # some actions with redis in future    
    
    await redis.close()

@app.on_event('shutdown')
async def shutdown():
    logger.info('server is stopping, connection to db is closing...')
    await database.disconnect()
    


@app.get('/')
def index():
    logger.info('visited index page')
    return {'status': "Working"}
