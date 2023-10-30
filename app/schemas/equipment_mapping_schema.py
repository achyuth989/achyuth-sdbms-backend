from pydantic import BaseModel
from datetime import datetime

class Equipment_Mapping(BaseModel):
    equipment_type_id:int=None
    equipment_name:str=None
    created_by_id:int=None

class Update_Equipment_Mapping(BaseModel):
    equipment_type_id:int=None
    equipment_name:str=None
    updated_by_id:int=None    

class Config():
    orm_mode=True    