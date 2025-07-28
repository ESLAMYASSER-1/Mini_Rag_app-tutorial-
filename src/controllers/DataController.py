from controllers import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from controllers import ProjectController
import re
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > int(self.FILE_MAXIMUM_SIZE):
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_UPLOADED_SUCCESS.value
    
    def generate_random_file_path(self, orig_file_name: str, project_id: str):


        random_key = self.generate_random_strings()
        project_path = ProjectController().GetProjectPath(project_id= project_id)
        new_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
            )
        new_file_path = os.path.join(project_path, random_key+"_"+new_file_name)


        while os.path.exists(new_file_path):
            random_key = self.generate_random_strings()

            project_path = ProjectController().GetProjectPath(project_id= project_id)
            new_file_name = self.get_clean_file_name(
                orig_file_name=orig_file_name
                )
            new_file_path = os.path.join(project_path, random_key+"_"+new_file_name)
            
        return new_file_path, random_key+"_"+new_file_name

    def get_clean_file_name(self, orig_file_name:str):
        clean_file_name = re.sub(r'[^\w.]', "", orig_file_name.strip())
        clean_file_name = clean_file_name.replace(" ", "_")

        return clean_file_name