from pydantic import BaseModel
from datetime import datetime,date
from typing import List
from typing import Any,Optional

class Infra_Questionary_List(BaseModel):
    site_asmt_infra_equal_id:Optional[int]
    question:str= None
    answer:str = None
    input:Optional[str]= None
    updated_by_id:Optional[int] = None


class Site_Asmt_Infrastructure(BaseModel):
    site_id: int
    questionaries:List[Infra_Questionary_List]
    created_by_id:int = None
    
class Update_Site_Asmt_Infra(BaseModel):
    question:str= None
    answer:str = None
    input:Optional[str]= None
    updated_by_id:Optional[int] = None
    

class Config:
    orm_mode=True  
