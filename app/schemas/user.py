from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    email:str  = None
    role_id:int = None
    name:str =None
    status:str = None
    created_by_id:int = None
    org_id:int=None
    

class UpdateUser(BaseModel):
    role_id:int = None
    status:str = None
    updated_by_id:int = None

class UserLogin(BaseModel):
    email:str  = None
    password:str = None
class Config:
    orm_mode = True
    
class User_Status_Schema(BaseModel):
    id : int
    updated_by_id : int = None