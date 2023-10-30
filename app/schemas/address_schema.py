from pydantic import BaseModel
from datetime import datetime

class Address(BaseModel):
    site_id:int =None
    as_per_license:str = None
    address_1:str = None
    address_2:str =None
    address_3:str = None
    address_4:str = None
    city:int = None
    district:str =None
    region:str =None
    pincode:str=None
    country:int =None
    created_by_id:int = None

    class Config:
        orm_mode = True