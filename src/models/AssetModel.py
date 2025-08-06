from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .DB_schemas import Asset
from bson.objectid import ObjectId


class AssetModel(BaseDataModel):
    def __init__(self, dbClient:object):
        super().__init__(dbClient=dbClient)
        self.collection = self.dbClient[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, dbClient:object):
        instance = cls(dbClient)
        await instance.init_collection()

        return instance
    
    async def init_collection(self):
        all_collections = await self.dbClient.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.dbClient[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index['name'],
                    unique=index['unique']
                )

    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(dict(asset))
        asset._id = result.inserted_id
        return asset
    
    async def get_all_projects_assets(self, asset_project_id, asset_type: str):
        records =  await self.collection.find({
            "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_type":asset_type,
        }).to_list(length=None)

         
        files = []
        for record in records:
            a = Asset(**record)
            a._id = record["_id"]
            files.append(a)
        return files
    
    async def get_project_assets_by_file_name(self, asset_project_id, asset_name: str):
        record =  await self.collection.find_one({
            "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_name":asset_name,
        })

         
        if record:
            a = Asset(**record)
            a._id = record["_id"]
            return a

        return None
        
    

