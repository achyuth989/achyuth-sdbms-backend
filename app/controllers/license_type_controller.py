from fastapi import APIRouter, Depends 
from app.schemas.license_type_schema import LicenseType,Updatelicensetype
from app.services.license_type_service import License_Type_Service
router = APIRouter(prefix="/api")
license_type_service = License_Type_Service()
@router.post("/licensetype")
def add_license_type(license_details : LicenseType):
    response = license_type_service.add_license_type(license_details)
    return response
# @router.get("/licensetype")
# def get_license_type():
#     response = license_type_service.license_type_list()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/licensetypes/{user_id}")
def get_license_types_related_to_org(user_id:int):
    response = license_type_service.license_type_list(user_id)
    return response

@router.put("/licensetype/{id}")
def update_license_type(id:int,LicenseType:Updatelicensetype):
    response = license_type_service.update_license_type(id,LicenseType)
    return response
@router.get("/licensetype/{id}")
def get_license_type(id:int):
    response = license_type_service.get_license_type(id)
    return response    
