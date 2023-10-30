from typing import List
from fastapi import APIRouter, Depends
from app.schemas.site_schema import Site, Update_Site, Site_Status
from app.services.site_service import Site_Service
router = APIRouter(prefix="/api")
site_service = Site_Service()
@router.post("/sites")
def add_sites(site_details : Site):
    response  =  site_service.add_site(site_details)
    return response
@router.get("/allsites/{user_id}")
def get_sites(user_id:int):
    response  =  site_service.sites_list(user_id)
    return response
@router.get("/activesites/{user_id}")
def get_sites(user_id:int):
    response  =  site_service.active_sites_list(user_id)
    return response

@router.get("/sites/{id}")
def get_sites_by_id(id:int):
    response = site_service.get_sites_list_by_id(id)
    return response
@router.put("/sites/{id}")
def update_site(id:int, data:Update_Site):
    response  =  site_service.update_site(id,data)
    return response    
@router.get("/institutioncontacts/{institution_id}")
def get_institution_contacts_by_id(institution_id:int):
    response = site_service.get_institution_contacts_by_id(institution_id)
    return response

@router.put("/sitestatus/{site_id}")
def update_site_status(site_id:int, data:Site_Status):
    response  =  site_service.update_site_status(site_id,data)
    return response    