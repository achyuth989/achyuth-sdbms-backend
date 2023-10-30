from pydantic import BaseModel
from datetime import datetime,date
from typing import List

class details(BaseModel):
    date:date
    salutation:str=None
    first_name:str=None
    last_name:str=None
    role:str=None
    contact_phone:int=None
    contact_email:str=None

class Site_Assess_Review(BaseModel):
    site_id:int=None
    evaluation_mode:str=None
    # reviewer_details:List[details]
    # user_department:List[details]
    # quality_assurance:List[details]
    created_by_id:int=None

class Update_Site_Assess_Review(BaseModel):
    evaluation_mode:str=None
    # reviewer_details:List[details]
    # user_department:List[details]
    # quality_assurance:List[details]
    updated_by_id:int=None    

class Config:
    orm_mode = True