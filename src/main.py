from fastapi import FastAPI
from pkg_resources import yield_lines
from routes import base,data
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pymongo import AsyncMongoClient


load_dotenv('.env')

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo_conn = AsyncMongoClient(os.getenv("MONGODB_URL"))
    app.db_client = app.mongo_conn[os.getenv("MONGODB_DATABASE")]

    yield
    await app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router= base.base_router)
app.include_router(router=data.data_router)
 