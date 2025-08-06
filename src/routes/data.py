from genericpath import getsize
import signal
from fastapi import APIRouter, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
import logging

from pydantic import FilePath


logger = logging.getLogger('uvicorn.error')


from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal, DataChunk, ChunkModel, AssetModel, Asset, AssetTypeEnum
from models.ProjectModel import ProjectModel
from routes import ProcessRequest


data_router = APIRouter(prefix="/api/v1/data", tags=['v1','data'])

@data_router.post('/upload/{project_id}')
async def upload_data(request: Request, project_id:str, file: UploadFile):
    project_model = await ProjectModel.create_instance(
        dbClient=request.app.db_client
        )
    
    project = await project_model.get_project_or_create_one(
        project_id=project_id
        )


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
    file_path, file_id = DataControllerOBJ.generate_random_file_path(file.filename, project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(int(DataControllerOBJ.FILE_CHUNK_SIZE)):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error While Uploading File: {e}")

        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={
                     "signal":ResponseSignal.FILE_UPLOADED_FAILED.value
                     }
            )
    #store asset in the database 
    asset_model = await AssetModel.create_instance(request.app.db_client)
    asset_resource = Asset(
        asset_project_id=  project._id,
        asset_type= AssetTypeEnum.FILE.value,
        asset_name= file_id,
        asset_size= os.path.getsize(file_path),  
    )
     
    asset_record = await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "signal":ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_ID":str(asset_record._id),
            }
        )



@data_router.post('/process/{project_id}')
async def process_endpoint(request:Request, project_id:str, processRequest: ProcessRequest):

    project_model = await ProjectModel.create_instance(
        dbClient=request.app.db_client
        )
    
    project = await project_model.get_project_or_create_one(
        project_id=project_id
        )
    

    chunk_model = await ChunkModel.create_instance(request.app.db_client)
    asset_model = await AssetModel.create_instance(request.app.db_client)
    
    chunk_size = processRequest.chunk_size
    overlap_size = processRequest.overlap_size
    do_reset = processRequest.do_reset

    project_file_ids={}
    if processRequest.file_id:
        asset_record = await asset_model.get_project_assets_by_file_name(
            asset_project_id=project._id,
            asset_name=processRequest.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "signal": ResponseSignal.FILE_ID_ERROR.value,
                }
            )
        project_file_ids = {
            asset_record._id:asset_record.asset_name
        }
    else:
       
        project_files = await asset_model.get_all_projects_assets(
            asset_project_id=project._id,
            asset_type=AssetTypeEnum.FILE.value,
        )
        project_file_ids = {
            record._id:record.asset_name
            for record in project_files
        }
    

    if len(project_file_ids)==0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "signal": ResponseSignal.NO_FILE_ERROR.value,
            }
        )
    



    process_cotroller = ProcessController(project_id)


    Num_records = 0
    Num_files = 0
    Num_bad_files = 0
    if do_reset ==1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project._id
        )
    for _id, file_id in project_file_ids.items():
        file_chunks = process_cotroller.process_file_content(file_id, chunk_size, overlap_size)

        if file_chunks is None or len(file_chunks)==0:
            logger.error(f"Error while processing file:{file_id}")
            Num_bad_files +=1
            continue
        
        file_chunks_records = [
            DataChunk(
                chunk_text= chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunck_order=i,
                chunk_project_id=project._id,
                chunk_asset_id = _id,
            )
            for i,chunk in enumerate(file_chunks)
            ]
        

        Num_records += await chunk_model.insert_many_chunks(file_chunks_records)
        Num_files +=1

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "signal":ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "# created chunks":Num_records,
            "# processed files": Num_files,
            "# Files that didn't processed": Num_bad_files,
        }
    )


