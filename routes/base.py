from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/", )
def welcome():
    return {'message': "App is running"}
