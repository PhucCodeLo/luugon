from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"

class CompressRequest(BaseModel):
    content: Optional[str] = Field(None, max_length=1000000, description="Text content to compress")
    type: ContentType = Field(..., description="Type of content: 'text' or 'image'")

class CompressResponse(BaseModel):
    item_id: UUID
    short_code: str
    short_url: str
    qr_code_url: Optional[str] = None  # Make it optional
    original_size_kb: int
    compressed_size_kb: int
    compression_ratio: float

class ItemResponse(BaseModel):
    id: UUID
    short_code: str
    content_type: ContentType = Field(..., alias="content_type")
    original_content: Optional[str] = None
    file_path: Optional[str] = None
    original_size_kb: int
    compressed_size_kb: int
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True

class ErrorResponse(BaseModel):
    detail: str
    status_code: int = 400
