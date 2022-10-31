from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import database, engine, async_session
from db.models import Base
import aioredis
from log import logger

from users.router import users as users_router
from invitations.router import router as inv_router
from companies.router import router as comp_router
from participants.router import router as part_router
from admins.router import router as admins_router

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
       # await conn.run_sync(Base.metadata.drop_all)
 
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


app.include_router(users_router)
app.include_router(comp_router)
app.include_router(inv_router)
app.include_router(part_router)
app.include_router(admins_router)


@app.on_event('startup')
async def startup():

    await init_models()

    logger.info('SERVER STARTED')
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
