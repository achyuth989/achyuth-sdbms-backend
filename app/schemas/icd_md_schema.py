from pydantic import BaseModel
from datetime import datetime
from typing import List

class icd(BaseModel):

   
    site_id:int = None
    # icd_code:str =None
    icd_code:List[str] = None
    created_by_id:int = None



    class Config:
        orm_mode = True