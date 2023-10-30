from fastapi import APIRouter, Depends
from app.schemas.site_services_schema import SiteServices,UpdateSiteServices
from app.services.site_services import Site_Services
router = APIRouter(prefix="/api")
site_services = Site_Services()
@router.post("/siteservices")
def add_site_services(site_service_details : SiteServices):
    response = site_services.add_site_services(site_service_details)
    return response
# @router.get("/siteservices")
# def get_site_services():
#     response = site_services.site_services_list()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/allsiteservices/{user_id}")
def get_site_services_related_to_org(user_id:int):
    response = site_services.site_services_list(user_id)
    return response

@router.put("/siteservices/{id}")
def update_site_service(id:int,SiteServices:UpdateSiteServices):
    response = site_services.update_site_service(id,SiteServices)
    return response
@router.get("/siteservices/{id}")
def get_site_services(id:int):
    response = site_services.get_site_services(id)
    return response    
@router.get("/filterservices/{id}")
def filter_site_services(id:int):
    response = site_services.filter_site_services(id)
    return response 