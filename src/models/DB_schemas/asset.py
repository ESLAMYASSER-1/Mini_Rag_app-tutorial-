from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Asset(BaseModel):
    _id: Optional[ObjectId]
    asset_project_id: ObjectId 
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(gt=0, default=None)
    asset_config: dict = Field(default={})
    asset_created_at: datetime = Field(default=datetime.now(timezone.utc))


    @classmethod
    def get_indexes(cls):

        return [
            {
                "key":[
                    ("asset_project_id", 1)
                ],
                "name": "asset_project_id_index_asc",
                "unique": False
            },
            {
                "key":[
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_and_name_index_asc",
                "unique": True
            }
        ]

    class Config:
        arbitrary_types_allowed = True