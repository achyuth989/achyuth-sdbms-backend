from pydantic import BaseModel
from  datetime import datetime
from typing import List, Optional

class Role_master(BaseModel):
    role:str = None
    role_description:str = None
    permissions:Optional[List[int]] = None
    created_by_id:int = None
    
class UpdateRolemaster(BaseModel):
    role_description:str = None
    permissions:Optional[List[int]] = None
    updated_by_id:int = None    

class StatusChange(BaseModel):
    updated_by_id:int=None     
    
class Config:
    orm_mode = True