from fastapi import FastAPI
from routes import base,data
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from stores import LLMProviderFactory
from controllers import BaseController


load_dotenv('.env')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startUP
    settings = BaseController()

    app.mongo_conn = AsyncMongoClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory()

    app.generation_client = llm_provider_factory.create(
                                                settings.GENERATION_BACKEND
                                                )
                                                
    app.generation_client.set_generation_model(
                                                settings.GENERATION_MODEL_ID
                                                )


    app.embedding_client = llm_provider_factory.create(
                                                settings.EMBEDDING_BACKEND
                                                )
    
    app.embedding_client.set_embedding_model(
                                                settings.EMBEDDING_MODEL_ID,
                                                settings.EMBEDDING_MODEL_SIZE
                                                )
    

    yield
    # On shultdown
    await app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router= base.base_router)
app.include_router(router=data.data_router)

