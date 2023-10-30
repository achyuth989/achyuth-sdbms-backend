from pydantic import BaseModel
from datetime import datetime

class ContactRole(BaseModel):
    contact_id:str = None
    contact_role:str = None
    description:str = None
    created_by_id:int = None

class UpdateContactRole(BaseModel):
    contact_role:str = None
    description:str = None
    updated_by_id:int = None

    class Config:
        orm_mode = True
