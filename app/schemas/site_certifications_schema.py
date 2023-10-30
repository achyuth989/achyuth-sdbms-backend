from pydantic import BaseModel
from datetime import datetime


class Site_Certificates(BaseModel):

    certification_id:str = None
    service_category_description:int = None
    certification_description:str = None
    created_by_id:int = None

class Updatesitecertifications(BaseModel):
    service_category_description:int = None
    certification_description:str = None
    updated_by_id:int = None


    class Config:
        orm_mode = True
