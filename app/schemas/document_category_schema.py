from pydantic import BaseModel
from datetime import datetime
class DocumentCategory(BaseModel):
    document_category :str = None
    description :str = None
    created_by_id :int = None
class Updatedocumentcategory(BaseModel):
    description :str = None
    updated_by_id :int = None
class Config:
    orm_mode = True
