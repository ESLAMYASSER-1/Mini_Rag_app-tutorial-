from fastapi import FastAPI, APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
import os
from controllers import DataController

data_router = APIRouter(prefix="/api/v1/data", tags=['v1','data'])

@data_router.post('/upload/{project_id}')
async def upload_data(project_id:str, file: UploadFile):
    
    #validate file properities
    is_valid, result = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result,
                "is_valid?":is_valid,
            }
        )
    
    return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "signal":result,
                "is_valid?":is_valid,
            }
        )

