from .BaseDataModel import BaseDataModel
from .DB_schemas import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    
    def __init__(self, dbClient:object):
        super().__init__(dbClient=dbClient)
        self.collection = self.dbClient[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    @classmethod
    async def create_instance(cls, dbClient:object):
        instance = cls(dbClient)
        await instance.init_collection()

        return instance
    
    async def init_collection(self):
        all_collections = await self.dbClient.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.dbClient[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index['name'],
                    unique=index['unique']
                )



    async def create_project(self, project: Project):
        result = await self.collection.insert_one(dict(project))
        project._id = result.inserted_id
        return project
    

    async def get_project_or_create_one(self, project_id:str):

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project

        project = Project(**record)
        project._id = record["_id"]
        return project
    
    async def get_all_projects(self, page: int=1, page_size: int=10):
        #cout total number of documents 
        total_documents = await self.collection.count_documents({})

        total_pages = total_documents//page_size
        if total_documents%page_size>0:
            total_pages+=1
        
        cursor = self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects = []

        async for document in cursor:
            projects.append(
                Project(**document)
            )
        return projects, total_pages
    

    

