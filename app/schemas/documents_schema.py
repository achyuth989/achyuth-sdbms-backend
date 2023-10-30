from pydantic import BaseModel
from datetime import datetime
from typing import List


class AdditionalDocuments(BaseModel):
    document_description:str=None
    short_name:str =None
    remarks:str=None
class Documents(BaseModel):
    site_id:int=None
    caterogy:int=None
    AdditionalDoc:List[AdditionalDocuments]
    created_by_id:int=None

class Update_Documents(BaseModel):
    site_id:int=None
    short_name:str =None
    document_description:str=None
    remarks:str=None
    updated_by_id:int=None  

class Config():
    orm_mode=True    