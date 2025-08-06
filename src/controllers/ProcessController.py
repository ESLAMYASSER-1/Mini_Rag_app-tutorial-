import os
from controllers import BaseController, ProjectController
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnums


class ProcessController(BaseController):
    def __init__(self, project_id:str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().GetProjectPath(self.project_id)
        
    def get_file_extension(self, file_id:str):
        return os.path.splitext(file_id)[-1]
    

    def get_file_loader(self, file_id:str):
        file_ext = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path,file_id)
        if not os.path.exists(file_path):
            return None
        if file_ext == ProcessingEnums.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
    
        if file_ext == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self, file_id:str):
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()
        return None
    
    def process_file_content(self, file_id:str, chunk_size:int =100, overlap_size:int = 20):
        file_content = self.get_file_content(file_id=file_id)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size= chunk_size,
            chunk_overlap = overlap_size,
            length_function = len
        )
        if not file_content:
            return None
        file_content_texts = [
            rec.page_content for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata for rec in file_content
        ]

        chunks = text_splitter.create_documents(file_content_texts, file_content_metadata)

        return chunks


    
    

    