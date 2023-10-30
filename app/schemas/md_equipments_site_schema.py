from pydantic import BaseModel
from datetime import datetime
from typing import List
class Equipment(BaseModel):
    site_id:int=None
    equipment_type:int=None
    equipment_name:List[str]=None
    created_by_id:int=None

class UpdateEquipmentStatus(BaseModel):
    updated_by_id:int=None    

class Config():
    orm_mode=True    