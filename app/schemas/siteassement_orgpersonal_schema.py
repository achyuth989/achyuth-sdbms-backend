from pydantic import BaseModel
from datetime import datetime
from typing import List

class Questions(BaseModel):
    question:str = None
    answer:str = None

class Roledetails(BaseModel):
    role:str =None
    salutation:str = None
    first_name:str = None
    last_name:str = None
    contact_phone:int = None
    contact_email:str = None
    
class Updateroledetails(BaseModel):
    # id: int
    role:str =None
    salutation:str = None
    first_name:str = None
    last_name:str = None
    contact_phone:int = None
    contact_email:str = None

class Siteassementorg(BaseModel):
    site_id:int = None
    organizations:List[Roledetails]
    questions:List[Questions]
    created_by_id:int = None

class Updatesiteassessment(BaseModel):
    questions:List[Questions]
    roles: List[Updateroledetails]
    updated_by_id:int =None

