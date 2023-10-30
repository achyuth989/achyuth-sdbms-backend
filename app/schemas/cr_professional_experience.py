from pydantic import BaseModel
from datetime import datetime,date
from typing import List
from typing import Any,Optional

class Pro_Certificates_List(BaseModel):
    cr_prof_exp_id:Optional[int]
    job_title:str= None
    institution_department:str = None
    year_started: date = None  
    year_completed: date = None  
    
class Licenses_List(BaseModel):
    cr_lic_ense_id:Optional[int]
    type_of_license:int
    license_issuer:str = None
    professional_license_number:str = None
    state_region :int
    country: int
    issue_date:date = None
    expiration_date:date = None
    
class Gcp_Trail_List(BaseModel):
    cr_res_exp_id:Optional[int]
    training_provider:str = None
    title_of_training:str = None
    version: str = None
    date_completed: date = None
    status: int

class Specialities_List(BaseModel):
    cr_theura_area_exp_id:Optional[int]
    specialities:int
    sub_specialities:int

class Total_Clinical_Exp_List(BaseModel):
    cr_tot_cli_res_exp_id:Optional[int]
    total_therapeutic_area:int
    total_sub_therapeutic_area:int
    sponsor_name: str = None
    cro_name:str = None
    no_of_completed_studies: int
    no_of_ongoing_studies: int
    start_date : date = None
    end_date : date = None
    status: int

class CrProfessionalExperience(BaseModel):
    cr_res_exp_check_list_id: Optional[int]
    site_id:int
    cr_code:str
    professional_certificate:List[Pro_Certificates_List] = None
    licenses: List[Licenses_List] = None
    gcp_trail: List[Gcp_Trail_List] = None
    study_type:List[str] = None
    clinical_study_phases :List[str] = None
    specialities:List[Specialities_List] = None
    total_clinical_exp: List[Total_Clinical_Exp_List] = None
    speciality_cie10 : str =None
    cv:int = None
    scanned_id:int = None
    scanned_title: int = None
    scanned_license: int = None
    IATA_training: int = None
    created_by_id:int
    
    
    
    
    
    


    
    
    