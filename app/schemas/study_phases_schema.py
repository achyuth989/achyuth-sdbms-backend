from pydantic import BaseModel
from datetime import datetime
class StudyPhases(BaseModel):
    phase_id :str  = None
    phases_type :str = None
    description :str = None
    created_by_id :int = None

class Updatestudyphases(BaseModel):
    phases_type :str = None
    description :str = None
    updated_by_id :int = None

class Config:
    orm_mode = True