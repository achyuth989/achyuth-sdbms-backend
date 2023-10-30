from pydantic import BaseModel
from datetime import datetime
from typing import List

class Questionary_List(BaseModel):
    question: str
    answer: int

class Legal(BaseModel):
    site_id:int=None
    questionaries :List[Questionary_List]
    created_by_id:int=None

class LegalUpdate(BaseModel):
    questionaries :List[Questionary_List]
    updated_by_id:int=None
