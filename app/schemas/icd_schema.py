from pydantic import BaseModel
from datetime import datetime

class ICD(BaseModel):
    icd_id: int
    icd_code: str
    description: str
    parent: str
    icd_level: int
    created_by_id: int
    created: datetime
    updated_by_id: int
    updated: datetime

class Config:
    orm_mode = True