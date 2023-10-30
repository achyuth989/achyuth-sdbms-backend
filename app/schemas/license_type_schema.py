from pydantic import BaseModel
from datetime import datetime
class LicenseType(BaseModel):
    license_id :str	= None
    license_type :str = None
    description	:str = None
    created_by_id :int = None

class Updatelicensetype(BaseModel):
    license_type :str = None
    description	:str = None
    updated_by_id :int = None

class Config:
    orm_mode = True