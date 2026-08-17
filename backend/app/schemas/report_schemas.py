from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportBase(BaseModel):
    title: str
    description: str

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    sanitized_content: Optional[str]
    image_url: Optional[str]
    status: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
