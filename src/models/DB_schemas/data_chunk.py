from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict 
    chunck_order: int
    chunk_project_id: ObjectId
    chunk_asset_id: ObjectId

    
    @classmethod
    def get_indexes(cls):

        return [
            {
                "key":[
                    ("chunk_project_id", 1)
                ],
                "name": "chunk_project_id_index_asc",
                "unique": False
            }
        ]
    class Config:
        arbitrary_types_allowed = True