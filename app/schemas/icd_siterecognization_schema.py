from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from typing import List,Optional

class orphans(BaseModel):
    orphan_icd_id:str =None 
    orphan_diseases_pathologies:str = None
    orphan_count_of_thread:str =None


class icds(BaseModel):
    top_icd_id:int
    top_diseases_pathologies:str
    top_count_of_thread:str
    

class Icdsite(BaseModel):

    site_id:int = None  
    top_icds: List[icds]
    question:int = None
    answer:str = None
    orphan_icds:Optional[List[orphans]]
    created_by_id:int


class updateicd(BaseModel):
    site_rec_icd_id:int= None
    top_icd_id:int
    top_diseases_pathologies:str
    top_count_of_thread:str

class  orphanicd(BaseModel):
    site_rec_icd_id:int= None
    orphan_icd_id:str =None 
    orphan_diseases_pathologies:str = None
    orphan_count_of_thread:str =None




class Updateicdsite(BaseModel):
    # site_id:int = None  
    top_icds: List[updateicd]
    orphan_icds:Optional[List[orphanicd]]
    question:int = None
    answer:str = None
    updated_by_id:int = None



    class Config:
        orm_mode = True
