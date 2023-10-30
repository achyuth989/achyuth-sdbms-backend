from pydantic import BaseModel
from datetime import datetime
from typing import List

class Questions(BaseModel):
    question:str=None
    answer:int=None  
    incrementid:int=None

class Specialities(BaseModel):
    specialities:int=None
    questions:List[Questions]  

class Rec_Population_Grp(BaseModel):
    site_id:int=None
    population_served:List[str]
    questions:List[Questions]
    specialities:List[Specialities]
    created_by_id:int=None

class Update_Rec_Population_Grp(BaseModel):
    population_served:List[str]
    questions:List[Questions]
    specialities:List[Specialities]
    updated_by_id:int=None