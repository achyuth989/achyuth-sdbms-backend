from pydantic import BaseModel
from datetime import datetime

class Cr_Status(BaseModel):
    cr_id:str=None
    cr_status:str=None
    description:str=None
    created_by_id:int=None

class Update_Cr_Status(BaseModel):
    cr_status:str=None
    description:str=None
    updated_by_id:int=None    

class Config():
    orm_mode=True    