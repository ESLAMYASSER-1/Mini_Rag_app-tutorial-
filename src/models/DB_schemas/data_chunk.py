from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict 
    chunck_order: int
    chunk_object_id: ObjectId


    class Config:
        arbitrary_types_allowed = True