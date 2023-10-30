from pydantic import BaseModel
from datetime import datetime
from typing import List,Set,Dict



class qns(BaseModel):
    question:str
    answer:List[str]
    type :str

class Specilities(BaseModel):
    question: str
    # answer:List[str]
    speciality_subspeciality_id: int  # Add the 'speciality_subspeciality_id' attribute
    count: int

class contacts(BaseModel):
    role:str 
    salutation:str
    first_name:str 
    last_name:str
    stand:str
    contact_phone:int 
    contact_email:str

class Sitehr(BaseModel):
    site_id:int = None
    questionary:List[qns]
    contactlist:List[contacts]
    specialities:List[Specilities]
    created_by_id:int = None




class Updateqns(BaseModel):
    site_rec_hr_id:int =None
    question:str
    answer:List[str]
    type :str

class Updatespecilities(BaseModel):
    site_rec_hr_id:int =None
    question: str
    answer:List[str]
    # type :str

class Updatecontacts(BaseModel):
    site_rec_hr_id:int =None
    role:str 
    salutation:str
    first_name:str 
    last_name:str
    stand:str
    contact_phone:int 
    contact_email:str 

class Updatesitehr(BaseModel):
    # site_rec_hr_id:int =None
    questionary:List[Updateqns]
    contactlist:List[Updatecontacts]
    specialities:List[Updatespecilities]
    updated_by_id:int = None




    class Config:
        orm_mode=True


