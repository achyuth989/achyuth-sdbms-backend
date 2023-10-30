from pydantic import BaseModel
from datetime import datetime
from typing import List

class Questionary_List(BaseModel):
    question: str
    answer:str = None
    input:str=None
    # type :str

class QualitySystems(BaseModel):
    site_id:int=None
    questionaries :List[Questionary_List]
    created_by_id:int=None

class QualitySystemsUpdate(BaseModel):
    questionaries :List[Questionary_List]
    updated_by_id:int=None
