from pydantic import BaseModel
from datetime import datetime

class Equipment_Type(BaseModel):
    equipment_code:str=None
    equipment_type:str=None
    equipment_description:str =None
    created_by_id:int=None

class Update_Equipment_Type(BaseModel):
    equipment_description:str =None
    updated_by_id:int=None    

class Config():
    orm_mode=True    