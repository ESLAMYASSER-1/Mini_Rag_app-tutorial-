from vectordb import QDrantDBProvider
from controllers import BaseController
from vectordb import VectorDBEnums

class VectorDBProviderFactory(BaseController):
    def __init__(self):
        pass 

    def create(self, provider:str):
        if provider == VectorDBEnums.QDRANT.value:


            return QDrantDBProvider(
                db_path=self.get_database_path(self.VECTOR_DB_PATH),
                distance_method=self.VECTOR_DB_DISTANCE_METHOD,
            )
        
        return None