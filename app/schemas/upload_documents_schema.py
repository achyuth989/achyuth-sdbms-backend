from pydantic import BaseModel
from datetime import datetime
from typing import List

class Versions(BaseModel):
    upload_document_id : int = None
    version:str = None
    attachment :str = None
    status :int  = None

class Details(BaseModel):
    document_name :str = None
    document_attached : str  = None
    versions :List[Versions] = None
    # status :int  = None
    remarks :str = None
    # attachment :str = None
    category :str = None
    # docid : int = None
class UploadDocuments(BaseModel):
    site_id :int  = None
    # Site_Population : List[Details] = None
    # Hospital_Infra : List[Details] = None
    # services : List[Details] = None
    Certifications : List[Details] = None
    # Equipment : List[Details] = None
    Cost_List : List[Details] = None
    # Cr_Infra : List[Details] = None
    # Cr_Infra_Phases: List[Details] = None
    # Cr_Infra_Research_Products: List[Details] = None
    # IT_Systems_Infra: List[Details] = None
    Human_Resources: List[Details] = None
    Regulatory_Information: List[Details] = None
    created_by_id :int = None
class Config:
    orm_mode = True