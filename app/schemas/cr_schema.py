from pydantic import BaseModel
from datetime import datetime
from typing import List

class Cr(BaseModel):
    site_id:int=None
    cr_code:str=None
    salutation:str=None
    first_name:str=None
    last_name:str=None
    speciality:str=None
    cr_experience:int=None
    certificate_of_good_clinical_practice:int=None
    role:int=None
    clinical_phases:List[int]
    cv_available:int=None
    cr_status:int=None
    created_by_id:int=None	

class CrUpdate(BaseModel):
    site_rec_cr_id: int=None
    cr_code:str=None
    salutation:str=None
    first_name:str=None
    last_name:str=None
    speciality:str=None
    cr_experience:int=None
    certificate_of_good_clinical_practice:int=None
    role:int=None
    clinical_phases:List[int]
    cv_available:int=None
    cr_status:int=None
    updated_by_id:int=None	



class Cr_Schema(BaseModel):
    Cr_List:List[Cr]=None

class Cr_Schema_Update(BaseModel):
    Cr_List:List[CrUpdate]=None

