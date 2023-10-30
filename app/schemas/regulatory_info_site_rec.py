from pydantic import BaseModel
from datetime import datetime,date
from typing import List
from typing import Optional

class Documents_List(BaseModel):
    site_rec_reg_info_id:Optional[int]
    document_category_id: int
    document: str
    availability:int
    date:date 
    remarks:str 
    updated_by_id:Optional[int]
    

class Regulatory_Information(BaseModel):
    site_id: int
    documents:List[Documents_List]
    created_by_id:int
    


# class Update_Documents_List(BaseModel):
#     status:int
#     date:date 
#     remarks:str = None
    
class Update_Regulatory_Information(BaseModel):
    # documents:List[Update_Documents_List]
    document:str
    availability:int
    date:date 
    remarks:Optional[str]
    updated_by_id:Optional[int] = None

class Config:
    orm_mode=True  
