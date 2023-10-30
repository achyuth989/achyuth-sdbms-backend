from pydantic import BaseModel
from datetime import datetime
from typing import List


class Geography(BaseModel):
    country_id:int=None
    city:str=None
    created_by_id:int=None

class Update_Geography(BaseModel):
    city:str=None
    updated_by_id:int=None

class Municipalities(BaseModel):
    municipality_id:List[int] 
    created_by_id:int=None  

class Update_Municipality(BaseModel):
    country_state_muni_id:int
    updated_by_id:int    

class Config:
    orm_mode=True    