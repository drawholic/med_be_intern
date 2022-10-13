from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import database, engine, Base
import aioredis
from users.main import users


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
    await database.connect()
    redis = await aioredis.from_url('redis://localhost')
    # some actions with redis in future    
    await redis.close()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    


@app.get('/')
def index():
    return {'status': "Working"}
