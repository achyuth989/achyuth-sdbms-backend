from pydantic import BaseModel
from  datetime import datetime


class DocumentStatus(BaseModel):
    document_status_id:str =  None
    document_status_description:str = None
    created_by_id:int = None

class Updatedocumentstatus(BaseModel):
    document_status_description:str = None
    updated_by_id:int = None


    class Config:
        orm_mode = True