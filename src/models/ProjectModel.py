from .BaseDataModel import BaseDataModel
from .DB_schemas import project


class ProjectModel(BaseDataModel):
    
    def __init__(self, dbClient:object):
        super().__init__(dbClient=dbClient)
        
