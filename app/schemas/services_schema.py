from pydantic import BaseModel
from  datetime import datetime
from typing import List
class Services(BaseModel):

    site_id:int = None
    service_category:int=None
    services_list:List[str]=None
    remarks:str = None
    created_by_id:int = None

class Updateservices(BaseModel):
    remarks:str = None
    services:int = None
    updated_by_id:int = None



    class Config:
        orm_mode = True