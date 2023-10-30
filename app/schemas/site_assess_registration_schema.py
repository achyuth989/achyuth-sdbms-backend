from pydantic import BaseModel
from datetime import datetime
from typing import List

class Questions(BaseModel):
    question:str=None
    answer:str=None

class Services(BaseModel):
    category_id:int=None
    services:str=None

class Site_Assess_Registration(BaseModel):
    site_id:int=None
    experience_in_studies:str=None
    category_services:List[Services]
    questions:List[Questions]=None
    created_by_id:int=None

class Update_Site_Assess_Registration(BaseModel):
    experience_in_studies:str=None
    category_services:List[Services]
    questions:List[Questions]=None
    updated_by_id:int=None

class Config:
    orm_mode = True