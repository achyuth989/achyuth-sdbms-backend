from pydantic import BaseModel
from datetime import datetime

class  Department(BaseModel):
    department_code :str = None
    department_name :str = None
    created_by_id:int = None
    
class Updatedepartment(BaseModel):
    department_name :str = None
    updated_by_id:int = None
    
class Config:
    orm_mode = True