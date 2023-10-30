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


class Site(BaseModel):
    site_code :str = None
    site_name :str = None
    institution_id :int = None
    address_1 :str = None
    address_2 :str = None
    address_3 :str = None
    address_4 :str = None
    # city :int = None
    country_state_muni_trn_id:int= None
    district :str = None
    region:str = None
    pin_code :str = None
    # country :int = None
    website :str = None
    smo_contacts:List[Contacts]
    site_contacts:List[Contacts]
    # responsible_sales_representative :int = None
    notes :str = None
    created_by_id :int = None

class Update_Site(BaseModel):
    institution_id :int = None
    address_1 :str = None
    address_2 :str = None
    address_3 :str = None
    address_4 :str = None
    country_state_muni_trn_id:int= None
    # city :int = None
    district :str = None
    region:str = None
    pin_code :str = None
    # country :int = None
    website :str = None
    smo_contacts:List[UpdateContacts]
    site_contacts:List[UpdateContacts]
    # responsible_sales_representative :int = None
    notes :str = None
    updated_by_id :int = None

class Site_Status(BaseModel):
    updated_by_id:int = None

class Config:
    orm_mode = True