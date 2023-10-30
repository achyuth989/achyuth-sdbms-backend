from pydantic import BaseModel
from datetime import datetime


class StudyType(BaseModel):
    study_type_id:str = None
    study_type:str = None
    description:str = None
    created_by_id:int = None

class Updatestudytypes(BaseModel):
    study_type:str = None
    description:str = None
    updated_by_id:int = None



    class Config:
        orm_mode = True