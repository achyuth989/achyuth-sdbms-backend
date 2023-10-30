from pydantic import BaseModel
from datetime import datetime,date
from typing import List
from typing import Any,Optional

class Questionary_List(BaseModel):
    site_rec_cr_infra_id:Optional[int]
    question: str= None
    answer: Any
    type: str
    updated_by_id:Optional[int] = None

class Research_List(BaseModel):
    site_rec_cr_infra_id:Optional[int]
    study_name: str= None
    type_of_study: str= None
    phase_id: str =None
    sponsor: str= None
    no_of_patients_recruited: int = None
    start_date: date = None        
    end_date: date = None
    updated_by_id:Optional[int] = None

class Cr_infra(BaseModel):
    site_id: int
    questionaries:List[Questionary_List]
    research: List[Research_List]
    # question: int
    # answer: int
    # phase_studies_ids: int
    # research_product_ids: int
    created_by_id:int
    # updated_by_id:int = None

# class Cr_infra_edit(BaseModel):
#     question:int=None
#     answer:int=None
#     updated_by_id:int=None
