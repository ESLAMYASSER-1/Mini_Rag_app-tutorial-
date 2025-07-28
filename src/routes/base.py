from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(prefix="/api/v1", tags=['v1'])

@base_router.get("/")
async def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {'message': f"{app_name}-{app_version} -is running!"}
