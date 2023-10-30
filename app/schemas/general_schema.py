from pydantic import BaseModel
from datetime import datetime
from typing import List

class Education(BaseModel):
    cr_gen_edu_id:int=None
    degree_certificate:str=None
    institution:str=None
    speciality:str=None
    year_completed:int=None

class UpdateEducation(BaseModel):
    cr_gen_edu_id:int=None
    degree_certificate:str=None
    institution:str=None
    speciality:str=None
    year_completed:int=None

class Affiliations(BaseModel):
    cr_gen_fac_aff_id:int=None
    primary_facility:str=None
    facility_department_name:str=None
    address:str=None

class UpdateAffiliations(BaseModel):
    cr_gen_fac_aff_id:int=None
    primary_facility:str=None
    facility_department_name:str=None
    address:str=None




class General(BaseModel):
    site_id:int=None
    cr_code:str=None
    salutation:str =None
    full_name:str=None
    # last_name:str=None
    speciality:int=None
    cr_experience:str=None
    good_clinical_practice:str = None
    role:int =None
    cv_available:str = None
    cr_status:int = None
    clinical_phases:List[int]
    created_by_id:int=None
    education:List[Education]
    affiliations:List[Affiliations]

class GeneralUpdate(BaseModel):
    # cr_code:str=None
    # cr_name:str=None
    # job_title:str=None
    # company_site_name:str=None
    # address_1:str=None
    # address_2:str=None
    # address_3:str=None
    # city:str=None
    # district:str=None
    # region:str=None
    # pincode:str=None
    # country:str=None
    # office_telephone:str=None
    # extension:str=None
    # mobile_telephone:str=None
    # email:str=None
    # website:str=None
    updated_by_id:int=None
    education:List[UpdateEducation]
    affiliations:List[UpdateAffiliations]

class FilterCr(BaseModel):
    site_id:int=None
    cr_id:int=None
    cr_status:int = None
    speciality_id:int = None    

class Reason(BaseModel):
    cr_id:int = None
    reason_for_blocking:str = None
    updated_by_id:int = None    
