from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
import os
import logging
logger = logging.getLogger('uvicorn.error')


from controllers import DataController, ProjectController
import aiofiles
from models import ResponseSignal

data_router = APIRouter(prefix="/api/v1/data", tags=['v1','data'])

@data_router.post('/upload/{project_id}')
async def upload_data(project_id:str, file: UploadFile):
    DataControllerOBJ = DataController()
    #validate file properities
    is_valid, result = DataControllerOBJ.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result,
                "is_valid?":is_valid,
            }
        )
    
    project_dir_path = ProjectController().GetProjectPath(project_id=project_id)
    file_path, file_di = DataControllerOBJ.generate_random_file_path(file.filename, project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(int(DataControllerOBJ.FILE_CHUNCK_SIZE)):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error While Uploading File: {e}")

        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={
                     "signal":ResponseSignal.FILE_UPLOADED_FAILED.value
                     }
            )
    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "signal":ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_ID":file_di
            }
        )


