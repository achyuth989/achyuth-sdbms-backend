from pydantic import BaseModel
from datetime import datetime
from typing import List

class Contacts(BaseModel):
    contact_name:str = None
    role:str = None
    office_telephone:int=None
    mobile_number:int=None
    extension:str=None
    email:str=None

class UpdateContacts(BaseModel):
    contact_id:int =None
    contact_name:str = None
    role:str = None
    office_telephone:int=None
    mobile_number:int=None
    extension:str=None
    email:str=None    


class Institution(BaseModel):
    institution_code:str=None
    institution_name:str=None
    address_1:str=None
    address_2:str=None
    address_3:str=None
    address_4:str=None
    # city:int=None
    # city:int=None
    district:str=None
    region:str=None
    pincode:str=None
    # country:int=None
    country_state_muni_trn_id:int= None
    # state:int= None
    smo_contacts:List[Contacts]
    institution_contacts:List[Contacts]
    website:str=None
    notes:str=None
    created_by_id:int=None

class Update_Institution(BaseModel):
    address_1:str=None
    address_2:str=None
    address_3:str=None
    address_4:str=None
    country_state_muni_trn_id:int= None
    # city:int=None
    district:str=None
    region:str=None
    pincode:str=None
    # country:int=None
    smo_contacts:List[UpdateContacts]
    institution_contacts:List[UpdateContacts]
    website:str=None
    notes:str=None
    updated_by_id:int=None

class Institution_Status(BaseModel):
    updated_by_id:int = None    


class Config:
    orm_mode = True