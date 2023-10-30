from pydantic import BaseModel
from datetime import datetime
from typing import List

class Details(BaseModel):
    document_name :str = None
    document_attached : str  = None
    version :str = None
    status :int  = None
    remarks :str = None
    attachment :str = None
    
class Cr_Doc_Upload(BaseModel):
    site_id :int  = None
    cr_code : int= None
    education_details : List[Details] = None
    affiliations_details : List[Details] = None
    cr_prof_exp_details : List[Details] = None
    cr_license_ense_details : List[Details] = None
    cr_gcp_trai_details : List[Details] = None
    # cr_specialities_details: List[Details] = None
    cr_Clinical_Research_Exp_details: List[Details] =None
    # collection
    clinical_study_phases: List[Details] = None
    study_type: List[Details] = None
    speciality_cie10: List[Details] = None
    cv: List[Details] = None
    scanned_id :List[Details] =None
    scanned_title :List[Details] =None
    scanned_license :List[Details] =None
    IATA_training :List[Details] =None
    created_by_id :int = None
    
class Versions(BaseModel):
    upload_document_id : int = None
    version:str = None
    attachment :str = None
    status :int  = None

    
class Edit_Details(BaseModel):
    # upload_document_id : int = None
    document_name :str = None
    document_attached : str  = None
    versions :List[Versions] = None
    # status :int  = None
    remarks :str = None
    # attachment :str = None
    
class Edit_Cr_Doc_Upload(BaseModel):
    site_id :int  = None
    cr_code : int= None
    education_details : List[Edit_Details] = None
    affiliations_details : List[Edit_Details] = None
    cr_prof_exp_details : List[Edit_Details] = None
    cr_license_ense_details : List[Edit_Details] = None
    cr_gcp_trai_details : List[Edit_Details] = None
    # cr_specialities_details: List[Edit_Details] = None
    cr_Clinical_Research_Exp_details: List[Edit_Details] =None
    # collection
    clinical_study_phases: List[Edit_Details] = None
    study_type: List[Edit_Details] = None
    speciality_cie10: List[Edit_Details] = None
    cv: List[Edit_Details] = None
    scanned_id :List[Edit_Details] =None
    scanned_title :List[Edit_Details] =None
    scanned_license :List[Edit_Details] =None
    IATA_training :List[Edit_Details] =None
    created_by_id :int = None

class Config:
    orm_mode = True