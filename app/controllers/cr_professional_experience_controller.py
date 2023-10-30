from typing import List
from fastapi import APIRouter, Depends
from app.schemas.cr_professional_experience import CrProfessionalExperience
from app.services.cr_professional_experience_service import Cr_Professional_Exp_Service

router = APIRouter(prefix="/api")
cr_professional_exp_service = Cr_Professional_Exp_Service()

@router.post("/cr-experience")
def add_and_update_cr_experience_new_details(cr_exp:CrProfessionalExperience):
    response = cr_professional_exp_service.add_cr_professional_exp_details(cr_exp)
    return response

@router.get("/cr-experience/{cr_code}")
def get_cr_experience_by_site_id(cr_code:int):
    response = cr_professional_exp_service.get_cr_professional_exp_details_by_site_id(cr_code)
    return response

@router.delete("/cr-experience/{primary_id}/{parameter}")
def delete_cr_exp_details_by_parameter_and_primary_id(primary_id:int,parameter:str):
    response = cr_professional_exp_service.delete_cr_professional_by_site_id_and_primary_id(primary_id,parameter)
    return response

@router.get("/cr-specialities")
def get_all_specialities_and_subspecialities_for_cr():
    response = cr_professional_exp_service.get_all_cr_specialities()
    return response