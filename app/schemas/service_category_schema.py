
from pydantic import BaseModel
from  datetime import datetime

class Service_Category(BaseModel):

    service_category:str = None
    description:str = None
    indicator:str = None
    created_by_id:int = None

class Updateservicecategory(BaseModel):
    description:str = None
    indicator:str = None
    updated_by_id:int = None
    
    
    
    class Config:
        orm_mode = True
