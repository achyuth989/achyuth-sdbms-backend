from pydantic import BaseModel,NoneStr
from datetime import datetime
from typing import List, Optional
class questions(BaseModel):
    question:str = None
    answer:str = None
    inputvalue : int = None
class services(BaseModel):
    service_category: int = None
    services: Optional[List[NoneStr]] = None
class hospitalinfra(BaseModel):
    site_id :int = None
    questionary:List[questions] = None
    service: List[services] = None
    certifications : List[str] = None
    equipment : List[str] = None
    created_by_id :int = None
    others_certifications:str = None
class updatehospitalinfra(BaseModel):
    questionary:List[questions] = None
    service: List[services] = None
    certifications : Optional[List[NoneStr]] = None
    equipment : Optional[List[NoneStr]] = None
    others_certifications:str = None
    updated_by_id :int = None
class Config:
    orm_mode = True