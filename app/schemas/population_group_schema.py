from pydantic import BaseModel
from datetime import datetime

class Population_Group(BaseModel):
    population_group_id:str=None
    population_group_description:str=None
    created_by_id:int=None

class Update_Population_Group(BaseModel):
    population_group_description:str=None
    updated_by_id:int=None    

class Config():
    orm_mode=True    