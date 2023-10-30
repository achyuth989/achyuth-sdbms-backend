from pydantic import BaseModel
from datetime import datetime
from typing import List

class Versions(BaseModel):
    upload_document_id : int = None
    version:str = None
    attachment :str = None
    status:int=None
class Details(BaseModel):
    document_name:str=None
    document_attached:str=None
    versions:List[Versions]=None
    # status:int=None
    remarks:str=None
    # attachment:str=None

class Upload_Site_Assess_Docs(BaseModel):
    site_id:int=None
    # experience_in_studies:List[Details]
    # outsourced_services:List[Details]
    # infra_equipment:List[Details]
    general:List[Details]
    legal:List[Details]
    created_by_id:int=None

class Update_Upload_Site_Assess_Docs(BaseModel):
    site_id:int=None
    # experience_in_studies:List[Details]
    # outsourced_services:List[Details]
    # infra_equipment:List[Details]
    general:List[Details]
    legal:List[Details]
    updated_by_id:int=None    