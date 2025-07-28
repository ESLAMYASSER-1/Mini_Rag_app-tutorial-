from fastapi import FastAPI
from routes import base,data
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()
app.include_router(router= base.base_router)
app.include_router(router=data.data_router)
