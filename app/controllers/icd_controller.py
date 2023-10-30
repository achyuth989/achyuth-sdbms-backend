from fastapi import APIRouter
from typing import List
from app.schemas.icd_schema import ICD
from app.services.icd_service import Icd_Service


router = APIRouter(prefix="/api")
icd_service = Icd_Service()

@router.get("/icd")
def get_icd_codes():
     icd10_codes = icd_service.get_icd_codes()
     return icd10_codes

# all 12000 records
@router.get("/icdall")
def get_all_icd_codes_in_db():
     icd10_codes = icd_service.get_all_icd_codes()
     return icd10_codes
# all 12000 records

@router.get("/geticdall")
def get_all_icd_codes_in_db():
     icd10_codes = icd_service.get_all_icds()
     return icd10_codes

@router.get("/sp_subsp")
def get_icd_codes():
     icd10_codes = icd_service.get_sub_speciality()
     return icd10_codes

@router.get("/Speciality_Subspeciality")
def get_icd_codes():
     sp_sub = icd_service.get_sub_speciality_speciality()
     return sp_sub

# date:25/08/2023 by achyuth
# this is from level-1 parents along with their chiilds(parent-child tree)
@router.get("/icd/page/{page_id}")
async def get_icd_codes_by_pagination(page_id: int):
     icd10_codes = icd_service.get_icd_codes_by_logic(page_id =page_id)
     return icd10_codes

@router.get("/icd/all")
async def get_icd_codes_by_querying():
     icd10_codes = icd_service.get_all_icd_codes_by_querying()
     return icd10_codes

# this for first 1000 records 
@router.get("/icd/{page_id}")
async def get_icd_codes_in_serial(page_id:int):
     icd10_codes = icd_service.get_icd_codes_by_id(page_id)
     return icd10_codes