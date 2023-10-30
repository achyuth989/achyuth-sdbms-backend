from pydantic import BaseModel
from datetime import datetime
from typing import List

class  Specialitiessubspecialities(BaseModel):
    icd_code:int =None
    therapeutic_area:int = None
    sub_therapeutic_area:int = None
    created_by_id:int = None

class Updatespecialities(BaseModel):
    icd_code:int = None
    therapeutic_area:int = None
    sub_therapeutic_area:int = None
    updated_by_id:int = None

class Dbspecialities(BaseModel):
    speciality_ids:List[str]=None  
    created_by_id:int = None  
    

class Config:
    orm_mode = True
