from pydantic import BaseModel
from datetime import datetime

class Crroles(BaseModel):
    cr_id:str = None
    cr_role:str = None
    description:str = None
    created_by_id:int = None

class Updatecrroles(BaseModel):
    cr_role:str = None
    description:str = None
    updated_by_id:int = None

    class Config:
        orm_mode = True
